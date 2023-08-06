from .ppt_insert_helper import PTT_Page_inserter
from .data_converter import CSV_Data_Converter
from .unitils import lazyproperty
from .logger_helper import logger
from .chart_element import Chartinfo
from typing import Literal, Self
from .dummy_iso_config import H3_05, simplifed_iso, H3_50, THOR, Q3, Q10


class Base_PPT_Report_Factory:

    def __init__(self):
        self.ppt_inserter = PTT_Page_inserter()
        self.coverter_cls = CSV_Data_Converter
        self.ppt_report = self.ppt_inserter.prs
        # 保存多次试验的数据转换器对象map
        self.data_converter_maps: dict[str, CSV_Data_Converter] = {}
        self.dummy_iso_config = {}  # 通过set_current_dummy来导入iso信息，只能保存一个假人的
        self.current_dummy_type: str = None  # 如"H3_50"
        self.current_seat_position_code: str = None  # 如”11“，”13“

    def from_other_factory(self, factory_instance: Self) -> Self:
        self.ppt_inserter = factory_instance.ppt_inserter
        self.ppt_report = factory_instance.ppt_report
        self.data_converter_maps = factory_instance.data_converter_maps
        self.dummy_iso_config = factory_instance.dummy_iso_config
        self.current_dummy_type = factory_instance.current_dummy_type
        self.current_seat_position_code = factory_instance.current_seat_position_code

        return self

    @property
    def current_seat_info(self) -> str:  # "DR:H3_50"
        position_mapper = {"11": "DR",
                           "13": "PS",
                           "14": "RL",
                           "16": "RR"}
        return position_mapper.get(self.current_seat_position_code, "Unknown") + ":" + self.current_dummy_type

    def create_full_prs(self, report_title: str = "Demo Report"):
        raise NotImplementedError(
            "Base PPT reporter full prs methord is not implemented!")

    def set_current_dummy(self, position_code: Literal["11", "13", "14", "16"],
                          dummy_type: Literal["H3_50", "H3_05", "THOR", "Q3", "Q10"]) -> Self:
        mapper = {
            "H3_50": H3_50,
            "H3_05": H3_05,
            "THOR": THOR,
            "Q3": Q3,
            "Q10": Q10
        }
        dummy_type_cls = mapper[dummy_type]  # 不存在会报错中断程序
        self.current_dummy_type = dummy_type
        self.current_seat_position_code = position_code

        dummy_iso_dict = dummy_type_cls(position_code).data
        self.dummy_iso_config = dummy_iso_dict
        return self

    def add_a_data_coverter(self, name: str, speed_kph: float, **kwargs) -> Self:
        converter = self.coverter_cls(name=name, speed_kph=speed_kph, **kwargs)
        self.data_converter_maps[name] = converter
        return self

    def save_ppt_report(self, output_file_name: str):
        self.ppt_report.save(output_file_name)
        logger.info(f"successfully save ppt file to {output_file_name}!")

    def chest_report(self):
        # 一般曲线
        chest_iso_dict = self.simplifyed_dummy_iso_config["chest"]
        self.create_gerneral_charts_with_seats_pages_by_iso_code(dummy_type=self.current_dummy_type,
                                                                 page_title="Chest analysis",
                                                                 **chest_iso_dict)
        # GS， ST，VT
        acc_keys = ["Chest_Acceleration_X",
                    'Chest_Acceleration_Y', "Chest_Acceleration_Z"]

        acc_iso_list = [chest_iso_dict[key] for key in acc_keys]
        chart_info_meta_list = []

        # GS, relative_VT,ST
        for acc_iso_code in acc_iso_list:  # 一次循环一张图
            mode = True if acc_iso_code[-2] == "X" else False
            direction = acc_iso_code[-2]

            gsr = Chartinfo.gs_relative_chart_meta(
                acc_iso_code, self.data_converter_maps, mode)
            chart_info_meta_list.append((gsr))
            rvt = Chartinfo.relative_vt_chart_meta(
                acc_iso_code, self.data_converter_maps, mode)
            chart_info_meta_list.append(rvt)
            rst = Chartinfo.relative_st_chart_meta(
                acc_iso_code, self.data_converter_maps, mode)
            chart_info_meta_list.append(rst)
            self.create_charts_in2pages_with_seats_info_by_chart_meta(
                page_title=f"Chest motion analysis {direction} Direction",
                chart_info_meta_list=chart_info_meta_list)
            chart_info_meta_list = []

        return self

    def head_report(self):
        # 一般曲线
        head_iso_dict = self.simplifyed_dummy_iso_config["head"]
        self.create_gerneral_charts_with_seats_pages_by_iso_code(dummy_type=self.current_dummy_type,
                                                                 page_title="Head analysis",
                                                                 **head_iso_dict)
        # GS， ST，VT
        acc_keys = ["Head_Acceleration_X",
                    'Head_Acceleration_Y', "Head_Acceleration_Z"]

        acc_iso_list = [head_iso_dict[key] for key in acc_keys]
        chart_info_meta_list = []

        # GS, relative_VT,ST
        for acc_iso_code in acc_iso_list:  # 一次循环一张图
            mode = True if acc_iso_code[-2] == "X" else False
            direction = acc_iso_code[-2]

            gsr = Chartinfo.gs_relative_chart_meta(
                acc_iso_code, self.data_converter_maps, mode)
            chart_info_meta_list.append((gsr))
            rvt = Chartinfo.relative_vt_chart_meta(
                acc_iso_code, self.data_converter_maps, mode)
            chart_info_meta_list.append(rvt)
            rst = Chartinfo.relative_st_chart_meta(
                acc_iso_code, self.data_converter_maps, mode)
            chart_info_meta_list.append(rst)
            self.create_charts_in2pages_with_seats_info_by_chart_meta(
                page_title=f"Head movtation analysis {direction} Dirextion",
                chart_info_meta_list=chart_info_meta_list)
            chart_info_meta_list = []

        return self

    def lumbar_report(self) -> Self:
        # 一般曲线
        lumbar_iso_dict = self.simplifyed_dummy_iso_config["lumbar"]
        self.create_gerneral_charts_with_seats_pages_by_iso_code(dummy_type=self.current_dummy_type,
                                                                 page_title="Lumbar analysis",
                                                                 **lumbar_iso_dict)
        return self

    def pelvis_report(self) -> Self:
        # 一般曲线
        pelvis_iso_dict = self.simplifyed_dummy_iso_config["pelvis"]
        self.create_gerneral_charts_with_seats_pages_by_iso_code(dummy_type=self.current_dummy_type,
                                                                 page_title="Pelvis analysis",
                                                                 **pelvis_iso_dict)
        return self

    def neck_upper_report(self):
        # 一般曲线
        neck_iso_dict = self.simplifyed_dummy_iso_config["neck_upper"]
        self.create_gerneral_charts_with_seats_pages_by_iso_code(dummy_type=self.current_dummy_type,
                                                                 page_title="Neck Upper analysis",
                                                                 **neck_iso_dict)
        return self

    def neck_lower_report(self):
        # 一般曲线
        neck_iso_dict = self.simplifyed_dummy_iso_config["neck_lower"]
        self.create_gerneral_charts_with_seats_pages_by_iso_code(dummy_type=self.current_dummy_type,
                                                                 page_title="Neck Lower analysis",
                                                                 **neck_iso_dict)
        return self

    def iliac_report(self):
        # 一般曲线
        iliac_iso_dict = self.simplifyed_dummy_iso_config["iliac"]
        self.create_gerneral_charts_with_seats_pages_by_iso_code(dummy_type=self.current_dummy_type,
                                                                 page_title="Iliac analysis",
                                                                 **iliac_iso_dict)
        return self

    def abdomen_report(self):
        # 一般曲线
        adbomen_iso_dict = self.simplifyed_dummy_iso_config["abdomen"]
        self.create_gerneral_charts_with_seats_pages_by_iso_code(dummy_type=self.current_dummy_type,
                                                                 page_title="Abdomen analysis",
                                                                 **adbomen_iso_dict)
        return self

    def seatbelt_force_report(self):
        # 一般曲线
        f_iso_dict = self.simplifyed_dummy_iso_config["seatbelt_force"]
        self.create_gerneral_charts_with_seats_pages_by_iso_code(dummy_type=self.current_dummy_type,
                                                                 page_title="seatbelt force analysis",
                                                                 **f_iso_dict)
        return self

    def legtibia_report(self):
        # 一般曲线
        all_tibia = ['tibia_left_upper', 'tibia_left_lower',
                     'tibia_right_upper', 'tibia_right_lower']
        for name in all_tibia:
            tibia = self.simplifyed_dummy_iso_config[name]
            self.create_gerneral_charts_with_seats_pages_by_iso_code(dummy_type=self.current_dummy_type,
                                                                     page_title="tibia analysis" + ":" + name,
                                                                     **tibia)
        return self

    def body_performance_report(self) -> Self:

        self.create_ppt_coverpage("Body performance analysis")
        chartinfo_list = []

        # GT,VT ,ST, GS 各个方向
        dirs = ["x", "y", "z"]
        value_typs = ["g", "v", "s"]
        for d in dirs:

            # GS曲线各个方向
            gschart = Chartinfo.body_GS_chartinfo(direction=d,
                                                  data_coverter_maps=self.data_converter_maps)
            chartinfo_list.append(gschart)

            # GT,VT ,ST各个方向
            for t in value_typs:
                tchart = Chartinfo.body_GTVTST_chartinfo(direction=d,
                                                         value_type=t,
                                                         data_coverter_maps=self.data_converter_maps)
                chartinfo_list.append(tchart)

        # s-s图
        sschart = Chartinfo.body_XY_ss_chartinfo(data_coverter_maps=self.data_converter_maps)
        chartinfo_list.append(sschart)

        # 图添加到幻灯片
        self.create_charts_in2pages_with_seats_info_by_chartinfo_instance(page_title="Body performance Analysis",
                                                                          chartinfo_list=chartinfo_list,
                                                                          seat_info="Body")

        # olc 分析
        self.olc_report()

        return self

    def olc_report(self, specify_isocode: str = None) -> Self:
        """生成OLC 报告

        :param str specify_isocode: 制定需要分析的波形isocode,只有在分析MPDB台车OLC用, defaults to None
        :return Self: ppt factory,支持链式调用
        """
        for name, dc in self.data_converter_maps.items():
            cdict = Chartinfo.OLC_VTST_chartinfos_dict(
                dc, specify_isocode=specify_isocode)
            if cdict is None:  # 输入的isocode 无效时候就不做图了
                logger.warn(f"输入的olc 分析用isocode {specify_isocode} 在 {str(dc)}中找不到，跳过做图！")
                return self
            vt_chart = cdict["vt_chart"]
            st_chart = cdict["st_chart"]
            summary = cdict["summary"]
            self.create_charts_in2pages_with_seats_info_by_chartinfo_instance(
                page_title=f"{name} Body OLC report" if specify_isocode is None else f"{name} {specify_isocode} OLC report",
                seat_info="Body",
                chartinfo_list=[vt_chart, st_chart], conclusion=summary
            )

        return self

    @lazyproperty
    def tests_names(self) -> list:
        return list(self.data_converter_maps.keys())

    def create_ppt_coverpage(self, ppt_title: str) -> Self:
        self.ppt_inserter.insert_cover_page(title=ppt_title)
        return self

    def create_gerneral_charts_with_seats_pages_by_iso_code(self, dummy_type: str,
                                                            page_title: str,
                                                            crash_direction: Literal["x",
                                                                                     "y"] = "x",
                                                            **kwargs):
        """一般图表报告输出

        Parameters
        ----------
        dummy_type : str
            如"AM50"
        **kwargs:
        要分析的iso_code, 如fz_iso_code=“11XXXXXXXX”

        """
        if not self.data_converter_maps:
            logger.warning(
                'PPT_factory未输入数据,请通过add_a_data_converter添加数据,否则无法生成此分析!')
            return self

        if not kwargs:
            logger.warning("至少需要一条iso code信息进行分析")
            return self

        iso_code_values = list(kwargs.values())

        seat_info = self.coverter_cls.confirm_seat_position_by_iso(
            iso_code_values[0]) + ":" + dummy_type

        charts_list = []

        for iso_code in iso_code_values:  # 一个iso_code就是一张图
            is_crash_direction = True if iso_code.strip(
            )[-2].lower() == crash_direction else False
            is_acc = CSV_Data_Converter.is_acc_by_iso(iso_code)
            transformed = is_crash_direction and is_acc  # 只有碰撞方向的ACC才需要矫正方向
            chart = Chartinfo.created_by_iso(iso_code=iso_code,
                                             data_converter_maps=self.data_converter_maps,
                                             transformed=transformed)
            if chart:
                charts_list.append(chart)

        self.ppt_inserter.insert_charts_with_seat_info(
            page_title=page_title,
            charts_info=charts_list,
            seat_info=seat_info,
        )
        return self

    @property
    def simplifyed_dummy_iso_config(self) -> dict:
        res = {}
        for part_name, full_config in self.dummy_iso_config.items():
            res[part_name] = simplifed_iso(full_config)
        return res

    def create_charts_in2pages_with_seats_info_by_chart_meta(self,
                                                             page_title: str,
                                                             chart_info_meta_list: list[dict]) -> Self:
        """根据图元信息生成图ppt页面,图元信息example 
        {
            'title':"chart A",
            'x_axis_title':"x_aixs"
            'y_axis_title':"y_aix",
            'series_meta':[
                {   'name': "series 1",
                    'x_data':[1,2],
                    'y_data':[3,4]
                },...],
        }

        Parameters
        ----------
        page_title : str
        chart_info_meta_list : list[dict]
           图元信息列表
        """
        charts_info_list = []
        for chart_meta in chart_info_meta_list:
            chart_info = Chartinfo.created_by_meta(chart_meta)
            charts_info_list.append(chart_info)

        self.ppt_inserter.insert_charts_with_seat_info(page_title, charts_info=charts_info_list,
                                                       seat_info=self.current_seat_info)
        return self

    def create_charts_in2pages_with_seats_info_by_chartinfo_instance(self,
                                                                     page_title: str,
                                                                     chartinfo_list: list[Chartinfo],
                                                                     seat_info: str = None,
                                                                     conclusion: str = None) -> Self:
        """根据图信息生成图ppt页面

        :param str page_title: 页面标题
        :param list[Chartinfo] chartinfo_list: 图实例信息list
        :return Self: 返回PPT工厂,支持链式调用
        """
        if seat_info is None:
            seat_info = self.current_seat_info

        self.ppt_inserter.insert_charts_with_seat_info(page_title, charts_info=chartinfo_list,
                                                       seat_info=seat_info, conclusion=conclusion)
        return self


class H3_50_PPT_Factory(Base_PPT_Report_Factory):

    def create_full_prs(self, report_title: str = "H3_50 Report") -> Self:
        self.create_ppt_coverpage(report_title)
        self.head_report()
        self.neck_upper_report()
        self.chest_report()
        self.legtibia_report()
        self.seatbelt_force_report()

        return self


class H3_05_PPT_Factory(Base_PPT_Report_Factory):

    def create_full_prs(self, report_title: str = "H3_05 Report") -> Self:
        self.create_ppt_coverpage(report_title)
        self.head_report()
        self.neck_upper_report()
        self.chest_report()
        self.iliac_report()
        self.seatbelt_force_report()
        return self


class THOR_PPT_Factory(Base_PPT_Report_Factory):

    def create_full_prs(self, report_title: str = "Thor Report") -> Self:
        self.create_ppt_coverpage(report_title)
        self.head_report()
        self.neck_upper_report()
        self.neck_lower_report()
        self.chest_report()
        self.abdomen_report()
        self.legtibia_report()
        self.seatbelt_force_report()
        return self

    def chest_report(self):  # Thor 胸部比较特殊重写方法
        # 一般曲线
        chest_iso_dict = self.simplifyed_dummy_iso_config["chest"]
        self.create_gerneral_charts_with_seats_pages_by_iso_code(dummy_type=self.current_dummy_type,
                                                                 page_title="Chest analysis",
                                                                 **chest_iso_dict)
        # GS， ST，VT
        # Thor 比较特殊胸部加速度用T4的XYZ
        t4 = self.simplifyed_dummy_iso_config["T4"]
        acc_keys = ['T4_Acceleration_X',
                    "T4_Acceleration_Z", "T4_Acceleration_Y"]

        acc_iso_list = [t4[key] for key in acc_keys]
        chart_info_meta_list = []

        # GS, relative_VT,ST
        for acc_iso_code in acc_iso_list:  # 一次循环一张图
            mode = True if acc_iso_code[-2] == "X" else False
            direction = acc_iso_code[-2]

            gsr = Chartinfo.gs_relative_chart_meta(
                acc_iso_code, self.data_converter_maps, mode)
            chart_info_meta_list.append((gsr))
            rvt = Chartinfo.relative_vt_chart_meta(
                acc_iso_code, self.data_converter_maps, mode)
            chart_info_meta_list.append(rvt)
            rst = Chartinfo.relative_st_chart_meta(
                acc_iso_code, self.data_converter_maps, mode)
            chart_info_meta_list.append(rst)
            self.create_charts_in2pages_with_seats_info_by_chart_meta(
                page_title=f"Chest movtation analysis {direction} Dirextion",
                chart_info_meta_list=chart_info_meta_list)
            chart_info_meta_list = []

        return self


class Q3_PPT_Factory(Base_PPT_Report_Factory):

    def create_full_prs(self, report_title: str = "Q3 Report") -> Self:
        self.create_ppt_coverpage(report_title)
        self.head_report()
        self.neck_upper_report()
        self.chest_report()
        return self


class Q10_PPT_Factory(Base_PPT_Report_Factory):

    def create_full_prs(self, report_title: str = "Q10 Report") -> Self:
        self.create_ppt_coverpage(report_title)
        self.head_report()
        self.neck_upper_report()
        self.chest_report()
        self.lumbar_report()
        self.pelvis_report()
        self.abdomen_report()
        self.seatbelt_force_report()
        return self
