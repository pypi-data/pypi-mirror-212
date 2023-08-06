import sys
import time
import os
import datetime

from django.db.models import Q
from django.db.models import F
from django.forms import model_to_dict

from utils.custom_tool import filter_result_field
from xj_invoice.utils.join_list import JoinList
from xj_thread.services.thread_list_service import ThreadListService
from xj_user.services.user_service import UserService
from ..services.invoice_extend_service import InvoiceExtendService
from ..utils.custom_tool import format_params_handle, force_transform_type, filter_fields_handler, dynamic_load_class, \
    write_to_log

from ..models import *


class InvoiceService:

    @staticmethod
    def add(params: dict = None, **kwargs):
        """
        发票添加
        :param params: 添加参数子字典
        :param kwargs:
        :return:
        """
        # 参数整合与空值验证
        params, is_void = force_transform_type(variable=params, var_type="dict", default={})
        kwargs, is_void = force_transform_type(variable=kwargs, var_type="dict", default={})
        params.update(kwargs)
        invoice_type = InvoiceType.objects.filter(invoice_type_code=params['invoice_type_code']).first()
        if not invoice_type:
            return None, "发票类型不存在"
        params['invoice_type_id'] = invoice_type.id
        # 过滤主表修改字段
        try:
            main_form_data = format_params_handle(
                param_dict=params.copy(),
                is_remove_empty=True,
                filter_filed_list=[
                    "user_id|int",
                    "thread_id|int",
                    "enroll_id_list",
                    "invoice_time|date",
                    "invoice_type_id|int",
                    "invoice_price|float",
                    "invoice_number",
                    "tax_rate",
                    "invoice_tax",
                    "invoice_untaxed",
                    "tax_number",
                    "operator_user_id|int",
                    'remark',
                    "invoice_status|int",
                    "destroy_name",
                    "destroy_date|date",
                    "destroy_reason",
                    "destroy_operator_id",
                    "email",
                    "invoice_snapshot|dict"

                ],
                alias_dict={},
                is_validate_type=True
            )
        except ValueError as e:
            # 模型字段验证
            return None, str(e)

        # 必填参数校验
        must_keys = ["thread_id", "user_id"]
        for i in must_keys:
            if not params.get(i, None):
                return None, str(i) + " 必填"

        # IO操作
        try:
            # 主表插入数据

            main_form_data['invoice_status'] = "APPLY"
            instance = Invoice.objects.create(**main_form_data)
            # 扩展表 插入或更新
            add_extend_res, err = InvoiceExtendService.create_or_update(params, instance.id)
        except Exception as e:
            return None, f'''{str(e)} in "{str(e.__traceback__.tb_frame.f_globals["__file__"])}" : Line {str(
                e.__traceback__.tb_lineno)}'''

        return {"id": instance.id}, None

    @staticmethod
    def edit(params: dict = None, invoice_id=None, search_param: dict = None, **kwargs):
        """
        发票编辑
        :param params: 修改的参数
        :param invoice_obj: 需要修改的发票主键
        :param search_param: 搜索参数, 服务层根据信息等其他搜索字段检索到需要修改的数据
        :return: data, err
        """
        # 空值检查
        params, is_pass = force_transform_type(variable=params, var_type="dict", default={})
        invoice_id, is_pass = force_transform_type(variable=invoice_id, var_type="int")
        search_param, is_pass = force_transform_type(variable=search_param, var_type="dict", default={})
        if not invoice_id and not search_param:
            return None, "无法找到要修改数据，请检查参数"
        # 搜索字段过滤
        if search_param:
            search_param = format_params_handle(
                param_dict=search_param,
                filter_filed_list=[
                    "invoice_id|int", "invoice_id_list|list", "thread_id|int", "thread_id_list|list",
                ],
                alias_dict={"invoice_id_list": "id__in", "thread_id_list": "thread_id__in"}
            )
        # 修改内容检查处理
        try:
            params = format_params_handle(
                param_dict=params,
                is_validate_type=True,
                is_remove_empty=True,
                filter_filed_list=[
                    "user_id|int",
                    "thread_id|int",
                    "enroll_id_list",
                    "invoice_time|date",
                    "invoice_type_id|int",
                    "invoice_price|float",
                    "invoice_number",
                    "tax_rate",
                    "invoice_tax",
                    "invoice_untaxed",
                    "tax_number",
                    "operator_user_id|int",
                    'remark',
                    "invoice_status|int",
                    "destroy_name",
                    "destroy_date|date",
                    "destroy_reason",
                    "destroy_operator_id",
                    "email",
                    "invoice_snapshot|dict"

                ],
            )
        except ValueError as e:
            return None, str(e)
        if not params:
            return None, "没有可修改的内容"

        # 构建ORM，检查是否存在可修改项目
        invoice_obj = Invoice.objects
        if invoice_id:
            invoice_obj = invoice_obj.filter(id=invoice_id)
        elif search_param:
            invoice_obj = invoice_obj.filter(**search_param)

        update_total = invoice_obj.count()
        if update_total == 0:
            return None, "没有找到可修改项目"

        # IO 操作
        try:
            invoice_obj.update(**params)
        except Exception as e:
            return None, "修改异常:" + str(e)
        return invoice_obj.first().to_json(), None

    @staticmethod
    def list(params):

        page = int(params['page']) - 1 if 'page' in params else 0
        size = int(params['size']) if 'size' in params else 10
        invoice = Invoice.objects
        invoice = invoice.order_by('-invoice_time')
        if params.get("is_all", 0) >= 1:
            params.pop("user_id")

        params = format_params_handle(
            param_dict=params,
            is_remove_empty=True,
            filter_filed_list=[
                "id|int", "id_list|list", "thread_id|int", "user_id|int", "invoice_type_code",
                "thread_id_list|list",
                "invoice_number|int",
                "invoice_time_start|date", "invoice_time_end|date"
            ],
            split_list=["thread_id_list", "id_list"],
            alias_dict={
                "invoice_time_start": "invoice_time__gte", "invoice_time_end": "invoice_time__lte",
                "thread_id_list": "thread_id__in", "id_list": "id__in",
                "invoice_type_code": "invoice_type__invoice_type_code__iexact"
            },
        )
        invoice = invoice.extra(select={'invoice_time': 'DATE_FORMAT(invoice_time, "%%Y-%%m-%%d %%H:%%i:%%s")'})
        invoice = invoice.annotate(invoice_typee_code=F("invoice_type__invoice_type_code"), )
        invoice = invoice.filter(**params).values()
        total = invoice.count()
        #
        current_page_set = invoice[page * size: page * size + size] if page >= 0 and size > 0 else invoice
        res_list = []
        for i, it in enumerate(current_page_set):
            it['order'] = page * size + i + 1
            it['invoice_time'] = it['invoice_time'].strftime("%Y-%m-%d %H:%M:%S")
            res_list.append(it)

        data = res_list
        # ========== 四、相关前置业务逻辑处理 ==========

        # ========== 五、翻页 ==========

        user_id_list = [item.get("user_id", None) for item in res_list]
        user_list, err = UserService.user_list(allow_user_list=user_id_list)
        if user_list:
            data = JoinList(res_list, user_list['list'], "user_id", "user_id").join()

        data = filter_result_field(
            result_list=filter_result_field(  # 扩展字段替换
                result_list=data,
                alias_dict={"id": "invoice_id"},
            ),
        )

        thread_id_list = [item.get("thread_id", None) for item in data]
        thread_list, err = ThreadListService.search(thread_id_list, filter_fields="title")
        if thread_list:
            data = JoinList(data, thread_list, "thread_id", "id").join()

        extend_id_list = [item.get("invoice_id", None) for item in data]
        extend_list, err = InvoiceExtendService.get_extend_info(extend_id_list)
        if extend_list:
            data = JoinList(data, extend_list, "invoice_id", "invoice_id").join()

        return {'size': int(size), 'page': int(page + 1), 'total': total, 'list': data, }, None

    @staticmethod
    def detail(invoice_id):
        if not invoice_id:
            return None, "发票id不能为空"
        invoice = Invoice.objects.filter(id=invoice_id).first()
        if not invoice:
            return None, "无法找到要修改数据，请检查参数"
        data = model_to_dict(invoice)
        extend_id_list = [data.get("id", None)]
        extend_list, err = InvoiceExtendService.get_extend_info(extend_id_list)
        if extend_list:
            data.update(extend_list[0])
        return data, None

    @staticmethod
    def examine_approve(params):
        invoice_id = params.get("invoice_id", 0)
        invoice_status = params.get("invoice_status", "")
        data = {}
        if not invoice_id:
            return None, "发票号不能为空"
        if invoice_status not in ["APPLY", "INVOIC", "RETURN", "CANCEL"]:
            return None, "未支持发票状态"
        data['invoice_status'] = invoice_status
        invoice_set = Invoice.objects.filter(id=invoice_id)
        invoice_update = invoice_set.update(**data)
        if not invoice_update:
            return None, "审核失败"
        invoice_obj = invoice_set.first()
        invoice_obj = model_to_dict(invoice_obj)
        return invoice_obj, None
