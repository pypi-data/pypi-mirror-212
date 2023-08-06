from flask import Blueprint, render_template, request, send_file, Response, session, redirect, g

import io
import json
import time
import sys
import time
import logging
import re

from functools import wraps
from datetime import datetime
from utah.core.content import BaseContentService, MicrositeNotFound
from utah.core.content import Doc
from utah.core.content import EHTMLDoc
from utah.core.content import TextDoc
from utah.core.content import ResourceHeader
from utah.core.content import EHTMLMetaData
from utah.core.content import Link
from utah.core.content import AuxContentRef
from utah.core.content import DocumentAlreadyExists
from utah.core.content import DocumentNotFound
from utah.core.content import FolderAlreadyExists
from utah.core.content import FolderDoesNotExist
from utah.core.content import create_dict_from_metadata
from utah.core.content import create_metadata_from_dict
from utah.core.content import parse_path
from utah.core import content
from utah.core.bootstrap import get_text_encoding
from jinja2.exceptions import TemplateNotFound
from utah.core.navigation import BaseNavigationService
from utah.arches.webtools import AuthorizationRootNavigationBean
from utah.arches.webtools import UserAuthorizationBean
from utah.core.utilities import ServiceFactory, get_service_object
from utah.core.utilities import func_logger
from utah.arches.webtools import get_user_id
from utah.core.authorize import URIAccessRight
from utah.arches.webtools import uri_authorized
from utah.core.authorize import BaseURIAuthorizationService
from utah.core.authorize import BaseGroupService
from utah.core.authorize import NoSuchGroupException
from utah.core.authorize import Group
from utah.arches.webtools import SkinService, validate_field
from flask_babel import gettext
from flask_babel import lazy_gettext
from flask_babel import format_datetime
from flask_babel import format_number

from utah.core.content import FOLDER_INVALIDATION_REGEX
from flask_restful import Resource, Api
import json

from utah.arches.webtools import URIUSE_ANY
from utah.arches.webtools import URIUSE_SESSION_ONLY
from utah.arches.webtools import URIUSE_TOKEN_ONLY


logger = logging.getLogger(__name__)

authorization_service:BaseURIAuthorizationService = get_service_object("uri_authorization")
group_service:BaseGroupService =  get_service_object("group_service")


content_mgmt_rights_definitions = [
("content_mgmt.%s.doc_rights",              "/content_mgmt/api/document/%s",                    ["GET","PUT","POST","DELETE"]),
("content_mgmt.%s.read_inherited_metadata", "/content_mgmt/api/inherited_metadata/%s",          ["GET"]),
("content_mgmt.%s.folder_rights",           "/content_mgmt/api/folder/%s",                      ["GET","POST","DELETE"]),
("content_mgmt.%s.move_rights",             "/content_mgmt/api/resource/move/%s",               ["POST"]),
("content_mgmt.%s.review_doc",              "/content_mgmt/review_doc/%s",                      ["GET"]),
("content_mgmt.layouts_info",               "/content_mgmt/api/layouts_info",                   ["GET"]),
("content_mgmt.layout",                     "/content_mgmt/api/layout",                         ["GET"]),
("content_mgmt.manageable_microsites",      "/content_mgmt/api/manageable_microsites",          ["GET"]),
("content_mgmt.load_navigation",            "/navigation/load",                                 ["GET"]),
("content_mgmt.manage_microsites",          "/content_mgmt/manage_microsites",                  ["GET"])
]



errors = {
    'UnauthorizedException': {
        'error_code':'UnauthorizedException',
        'message': gettext("User Not logged in"),
        'status': 401
    },
    'ForbiddenException': {
        'error_code':'ForbiddenException',
        'message': gettext("Authorization Error"),
        'status': 403
    },
    'FolderDoesNotExist' : {
        'error_code':'FolderDoesNotExist',
        'message': gettext("Folder does not exist"),
        'status': 404
    },
    'FolderAlreadyExists' : {
        'error_code':'FolderAlreadyExists',
        'message': gettext("Folder by that name already exists within parent folder"),
        'status': 409
    },
    'DocumentNotFound' : {
        'error_code':'DocumentNotFound',
        'message': gettext("Document does not exist"),
        'status': 404
    },
    'DocumentAlreadyExists' : {
        'error_code':'DocumentAlreadyExists',
        'message': gettext("Folder by that name already exists within parent folder"),
        'status': 409
    },
    'InvalidDocTypeException' : {
        'error_code':'InvalidDocTypeException',
        'message': gettext("Cannot load binary documents via the API"),
        'status': 409
    },
    'InvalidApiParameter' : {
        'error_code':'InvalidApiParameter',
        'message': gettext("An invalid parameter was supplied to the API"),
        'status': 409
    },
    'MicrositeAlreadyExists' : {
        'error_code':'MicrositeAlreadyExists',
        'message': gettext("Microsite Already Exists"),
        'status': 409
    },
    'MicrositeNotFound' : {
        'error_code':'MicrositeNotFound',
        'message': gettext("Microsite does not exist"),
        'status': 404
    },
    'DeleteMainMicrositeAttempted' : {
        'error_code':'DeleteMainMicrositeAttempted',
        'message': gettext("Cannot delete main microsite"),
        'status': 409
    }
}

class InvalidInputException(Exception):
    pass

class InvalidDocTypeException(Exception):
    pass

class InvalidApiParameter(Exception):
    pass


def render_ehtml(doc, document_path):
    resp_payload = render_template("content/ehtml_content.html", doc=doc)
    return resp_payload, False


def render_text(doc, document_path):
    return doc.text, True


def render_binary(doc, document_path):
    return doc.doc_bytes, True



app = Blueprint('content', __name__,url_prefix="/")
api = Api(app, errors=errors)


RENDERERS = {   content.RENDER_TYPE_BINARY:render_binary,
                content.RENDER_TYPE_TEXT:render_text,
                content.RENDER_TYPE_EHTML:render_ehtml
}


content_service:BaseContentService = get_service_object("content")
layout_service:SkinService = get_service_object("layout")

def doc_to_json(doc):
    ret_json = None
    if doc.resource_header.render_type == content.RENDER_TYPE_TEXT:
        ret_json = {"text" : doc.text}

    elif doc.resource_header.render_type == content.RENDER_TYPE_EHTML:
        ret_json = {"text" : doc.text, "metadata" : create_dict_from_metadata(doc.metadata)}

    else:
        ret_json = {
            "size" : format_number(len(doc.doc_bytes))
        }

    ret_json["last_modified_date"] = format_datetime(doc.last_modified_date, "medium")

    return ret_json


class MicrositeInventory(Resource):
    def get(self, microsite):
        mi = content_service.get_microsite_inventory(microsite)
        ri = {}

        for uri in mi:
            mii = mi[uri]
            d = {}
            ri[uri] = d
            d["uri"] = uri
            d["is_folder"] = mii.is_folder
            d["last_modified_date"] = mii.last_modified_date
            d["size"] = mii.size
        return ri



class LayoutsInfo(Resource):
    @uri_authorized(URIUSE_ANY)
    def get(self):
        i18n_layouts = {}
        i18n_aux_content_types = {}

        ret_value = {}
        ret_value["layouts"] = i18n_layouts
        ret_value["aux_content_types"] = i18n_aux_content_types
        ret_value["default_layout"] = layout_service.get_default_layout()
        ret_value["default_aux_content_type"] = layout_service.get_default_aux_content_type()

        layouts = layout_service.get_layouts()

        for key in layouts.keys():
            i18n_layout = {}
            i18n_layout["description"] = gettext(layouts[key]["description"])
            i18n_layout["supported_aux_content_types"] = layouts[key]["supported_aux_content_types"]
            i18n_layouts[key] = i18n_layout


        aux_content_types = layout_service.get_aux_content_types()

        for key in aux_content_types.keys():
            i18n_aux_content_types[key] = gettext(aux_content_types[key])

        return ret_value


class MicrositeList(Resource):
    @uri_authorized(URIUSE_ANY)
    def delete(self, microsite):
        content_service.delete_microsite(microsite)
        group_name = "content_mgmt-%s" % microsite
        group = group_service.get_group(group_name)
        if group:
            group_service.delete_group(group_name)


        for right_definition in content_mgmt_rights_definitions:
            (name, temp_uri, methods) = right_definition
            if name.find('%s') > -1:
                right_name = name % microsite
            else:
                right_name = name

            right:URIAccessRight = authorization_service.get_authorization(right_name)
            if right:
                if name.find('%s') > -1:
                    authorization_service.delete_authorization(right_name)
                else:
                    if group_name in right.authorized_groups:
                        right.authorized_groups.remove(group_name)
                        authorization_service.update_authorization(right)

        return {"status" : "deleted"}


    @uri_authorized(URIUSE_ANY)
    def post(self, microsite):
        content_service.create_microsite(microsite)
        microsite_path = "/%s" % microsite
        content_service.create_folder(microsite_path, "__system")
        content_service.create_folder(microsite_path, "js")
        content_service.create_folder(microsite_path, "css")
        content_service.create_folder(microsite_path, "images")
        content_service.create_folder(microsite_path, "spiffs")

        metadata_doc = EHTMLDoc(ResourceHeader("/%s/__system/metadata.html" % microsite), EHTMLMetaData(), "", get_text_encoding())
        content_service.create_document(metadata_doc)

        group = group_service.get_group("content_mgmt-%s" % microsite)
        if not group:
            group = Group("content_mgmt-%s" % microsite, "Content Managers for Microsite %s" % microsite)
            group_service.add_group(group)

        for right_definition in content_mgmt_rights_definitions:
            (name, temp_uri, methods) = right_definition
            if name.find('%s') > -1:
                right_name = name % microsite
                uri = temp_uri % microsite
            else:
                right_name = name
                uri = temp_uri

            right = authorization_service.get_authorization(right_name)
            if not right:
                uri_access_right = URIAccessRight(right_name, uri, methods, [], [group.name])
                authorization_service.add_authorization(uri_access_right)
            else:
                if not group.name in right.authorized_groups:
                    right.authorized_groups.append(group.name)
                    authorization_service.update_authorization(right)

        return {"status" : "created"}


class ManageableMicrosites(Resource):
    @uri_authorized(URIUSE_ANY)
    def get(self):
        user_id = get_user_id()
        method = "POST"

        microsite_names = content_service.get_microsite_names()

        ret_uris = []

        for microsite_name in microsite_names:
            if authorization_service.is_authorized_request(user_id, "/content_mgmt/api/document/" + microsite_name, method):
                ret_uris.append("/" + microsite_name)

        return ret_uris


def get_locale_str():
    locale_str = None

    if "locale" in request.args:
        locale_str = request.args["locale"]
    else:
        locale_str = g.locale

    return locale_str

class InheritedMetadata(Resource):
    @uri_authorized(URIUSE_ANY)
    def get(self, document):

        locale_str = get_locale_str()

        main_microsite = content_service.get_main_microsite()
        segs = document.split("/")

        uri = None
        doc = None
        # Are we getting inherited data for a metadata doc
        if document.endswith("/" + content.METADATA_DOC_DIR + "/" + content.METADATA_DOC_NAME):
            # Are we getting inherited data for the main microsite metadata doc
            if segs[0] == main_microsite:
                ret_json = {    "text" : "", 
                                "metadata" : {
                                    "layout" : "",
                                    "title" : "",
                                    "keywords" : "",
                                    "suppress_inheritance" : False,
                                    "extended_attributes" : {},
                                    "description" : "",
                                    "aux_content_refs" : [],
                                    "scripts" : [],
                                    "links" : []
                                }}
            else:
                uri = "/%s/%s/%s" % (main_microsite, content.METADATA_DOC_DIR, content.METADATA_DOC_NAME)
                doc = content_service.get_uncached_document(uri, locale_str)
                ret_json = doc_to_json(doc)
        else:
            uri = "/%s/%s/%s" % (segs[0], content.METADATA_DOC_DIR, content.METADATA_DOC_NAME)
            doc = content_service.get_uncached_document(uri, locale_str)
            ret_json = doc_to_json(doc)


        return ret_json



class Layout(Resource):
    @uri_authorized(URIUSE_ANY)
    def get(self, name):
        ret_value = {}
        ret_value["name"] = name
        tmpl = layout_service.get_layout(name)
        ret_value["description"] = tmpl["description"]
        all_aux_content_types = layout_service.get_aux_content_types()

        supported_aux_content_types = []
        for aux_content_type in tmpl["supported_aux_content_types"]:
            supported_aux_content_types.append({"type":aux_content_type, "description":all_aux_content_types[aux_content_type]})

        ret_value["supported_aux_content_types"] = supported_aux_content_types

        return ret_value


class Folder(Resource):
    @uri_authorized(URIUSE_ANY)
    def get(self, folder):
        folder_obj = content_service.get_folder("/" + folder)

        file_list = []

        ret_dict = {
            "child_folders" : folder_obj.child_folders,
            "files" : file_list,
        }

        for file_resource_header in folder_obj.file_resource_headers:
            file_dict = {
                "uri":file_resource_header.uri,
                "mimetype":file_resource_header.mimetype,
                "resource_id":file_resource_header.resource_id,
                "render_type":file_resource_header.render_type            
            }

            file_list.append(file_dict)

        return ret_dict

    @uri_authorized(URIUSE_ANY)
    def post(self, folder):
        last_slash = folder.rfind("/")
        parent_folder = "/" + folder[:last_slash]
        folder_name = folder[last_slash+1:]

        content_service.create_folder(parent_folder, folder_name)


    @uri_authorized(URIUSE_ANY)
    def delete(self, folder):
        content_service.delete_folder("/" + folder)


class Document(Resource):
    @uri_authorized(URIUSE_ANY)
    def get(self, document):
        uri = "/" + document
        locale_str = get_locale_str()

        if not "option" in request.args:
            option = "raw"
        else:
            option = request.args.get("option")

        doc = None
        if option == "raw":
            doc = content_service.get_raw_document(uri, locale_str=None)

        elif option == "cached":
            doc = content_service.get_document(uri, locale_str=locale_str)

        elif option == "uncached":
            locale_str = get_locale_str()
            doc = content_service.get_uncached_document(uri, locale_str, locale_str=locale_str)

        else:
            raise InvalidApiParameter("option must be one of the following values:['raw','cached','uncached']")


        if not doc:
            raise DocumentNotFound("")

        return doc_to_json(doc)


    @uri_authorized(URIUSE_ANY)
    def delete(self, document):
        uri = "/" + document
        content_service.delete_document(uri)

        return {"status":"ok"}


    @uri_authorized(URIUSE_ANY)
    def post(self, document):
        uri = "/" + document

        if 'file' not in request.files:
            request_payload = request.get_json()
            resource_header = ResourceHeader(uri)
            new_doc = None

            if resource_header.render_type == content.RENDER_TYPE_EHTML:
                metadata = EHTMLMetaData()
                new_doc = EHTMLDoc(resource_header, None, "", get_text_encoding())

            elif resource_header.render_type == content.RENDER_TYPE_TEXT:
                new_doc = TextDoc(resource_header, "", get_text_encoding())
            else:
                raise InvalidInputException("System cannot create a document of type:[%s] uri passed was:[%s]" % (resource_header.mimetype, uri))


            self.update_doc_from_json(new_doc, request_payload)

            content_service.create_document(new_doc)
        else:
            file = request.files['file']
            content_service.write_file(uri, file)

        return {"status":"ok"}


    @uri_authorized(URIUSE_ANY)
    def put(self, document):
        uri = "/" + document

        doc = content_service.get_raw_document(uri)
        if not doc:
            raise DocumentNotFound("Not document was found at uri:[%s]" % uri)


        request_payload = request.get_json()

        self.update_doc_from_json(doc, request_payload)

        content_service.update_document(doc)

        return {"status":"ok"}


    def update_doc_from_json(self, doc, request_payload):
        if doc.resource_header.render_type == content.RENDER_TYPE_TEXT:
            doc.text = request_payload["text"]

        elif doc.resource_header.render_type == content.RENDER_TYPE_EHTML:
            doc.text = request_payload["text"]
            metadata = create_metadata_from_dict(request_payload["metadata"])
            doc.metadata = metadata
        else:
            raise InvalidDocTypeException("Cannot write binary document via this API")




class Mover(Resource):
    @uri_authorized(URIUSE_ANY)
    def post(self, microsite):
        #raise DocumentAlreadyExists("ugh!!")
        request_payload = request.get_json()
        if request_payload["is_folder"]:
            content_service.move_folder(request_payload["from_uri"], request_payload["to_uri"])
        else:
            content_service.move_document(request_payload["from_uri"], request_payload["to_uri"])

        return {"status":"ok"}


api.add_resource(MicrositeList, '/content_mgmt/api/microsite_list/<microsite>')

api.add_resource(Document, '/content_mgmt/api/document/<path:document>')
api.add_resource(InheritedMetadata, '/content_mgmt/api/inherited_metadata/<path:document>')
api.add_resource(Folder, '/content_mgmt/api/folder/<path:folder>')
api.add_resource(Mover, '/content_mgmt/api/resource/move/<microsite>')

api.add_resource(LayoutsInfo, '/content_mgmt/api/layouts_info')
api.add_resource(Layout, '/content_mgmt/api/layout/<name>')
api.add_resource(ManageableMicrosites, '/content_mgmt/api/manageable_microsites')
api.add_resource(MicrositeInventory, '/content_mgmt/api/microsite_inventory/<microsite>')


@app.route("content_mgmt/manage_microsites", methods=['GET'])
@uri_authorized(URIUSE_SESSION_ONLY)
def manage_microsite():
    return render_template("content/manage_microsites.html")



@app.route("content_mgmt/archive/<microsite>", methods=['GET'])
@uri_authorized(URIUSE_SESSION_ONLY)
def archive_microsite(microsite):
    try:
        reader=content_service.create_microsite_archive(microsite)
        return Response(reader, content_type="application/zip")

    except MicrositeNotFound as e:
        status = 404
        path = "/%s/%s" % (content_service.get_main_microsite(), "/__system/error_pages/404.html")
        doc = content_service.get_document(path, g.locale)

        (resp_payload, ok_to_cache) = render_ehtml(doc, path)

        resp = Response(
            response=resp_payload,
            status=status)

        return resp





@app.route("content_mgmt/review_doc/<path:document_path>.html", methods=['GET'])
@uri_authorized(URIUSE_SESSION_ONLY)
def review_doc(document_path):
    document_path = "/%s.html" % document_path

    doc=content_service.get_uncached_document(document_path, get_locale_str())

    (payload, layed_out) = render_ehtml(doc, document_path)

    return payload


@app.route("/<path:document_path>", methods=['GET'])
@uri_authorized(URIUSE_SESSION_ONLY)
def getDocument(document_path):
    return _getDocument(document_path, get_locale_str())


def _getDocument(document_path, locale_str:str=None):
    status = None
    headers = {}
    resp_payload = None

    doc = None
    if "Referer" in request.headers:
        if not request.headers["Referer"].find("/content_mgmt/review_doc/") == -1:
            (path, name, locale_str, extension) = parse_path(request.headers["Referer"])

    try:
        status = 200
        document_path = "/" + document_path
        doc = content_service.get_document(document_path, locale_str)

        if not doc:
            status = 404
            doc = content_service.get_document("/%s/%s" % (content_service.get_main_microsite(), "/__system/error_pages/404.html"), locale_str)

        if not doc:
            raise DocumentNotFound()

        str_last_modified = doc.last_modified_date.strftime("%a, %d %b %Y %H:%M:%S UTC")

        im = None
        if "If-Modified-Since" in request.headers:
            im = request.headers["If-Modified-Since"]

        if im == str_last_modified and not doc.resource_header.render_type == content.RENDER_TYPE_EHTML:
            status = 304
            resp_payload = None
        else:
            resp_payload, ok_to_cache = RENDERERS[doc.resource_header.render_type](doc, document_path)
            headers["Content-Type"] = doc.resource_header.mimetype
            headers["Content-Encoding"] = doc.resource_header.mime_encoding
            if ok_to_cache:
                headers["Last-Modified"] = str_last_modified
            else:
                headers["Cache-Control"] = "no-cache"


    except TemplateNotFound as e:
        resp_payload = gettext("Bad Layout [layouts/layout_%(layout)s.html] was specified, review document [%(document_path)s]", layout=doc.metadata.layout, document_path=document_path)
        status = 500

    except Exception as e:
        logger.exception(e)
        resp_payload = """
        <html>
            <head>
                <title>%s</title>
            </head>
            <body style="background-color: brown; color:bisque;">
                %s
            </body>
        </html>
        """ % (gettext("Error Page"), gettext("Oh boy is our face red!!! This site cannot even display an error page properly at this time."))
        status = 500

    resp = Response(
            response=resp_payload,
            status=status,
            headers=headers
    )

    return resp


@app.route("content_mgmt/reload_from_repo", methods=['GET'])
@uri_authorized(URIUSE_SESSION_ONLY)
def reload_from_repo():
    status = content_service.reload_from_repo()

    if status:
        return gettext("Content repository was reloaded sucessfully")
    else:
        return gettext("Content repository reload failed. Please consult your system administrator")