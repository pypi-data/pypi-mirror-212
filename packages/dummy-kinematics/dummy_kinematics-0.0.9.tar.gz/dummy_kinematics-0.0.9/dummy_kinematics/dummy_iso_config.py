
import json
import copy


def simplifed_iso(part_dict: dict):
    return {k: v["code"] for k, v in part_dict.items()}


class Base_Dummy:

    __field__ = []  # 需要指定生成json的字典名称

    def __init__(self, position_code: str):
        self.position_code = str(position_code)
        self.data: dict = self._add_position_code()

    def _add_position_code(self) -> dict:
        data = {}
        for field in self.__field__:
            _part_dict = getattr(self, field)  # 类变量不要被污染了
            part_dict = copy.deepcopy(_part_dict)  # 深拷贝类变量
            for k, value_dict in part_dict.items():
                # 更新code值，加上位置代码如“11”
                value_dict["code"] = self.position_code+value_dict["code"]
            data[field] = part_dict
        return data

    def to_json_file(self, file_name: str):
        with open(file_name, "w") as f:
            json.dump(self.data, f, indent=4)
        print(f"successufuly write in the file: {file_name}")


class H3_50(Base_Dummy):

    __field__ = ["head", 'neck_upper', "chest", "pelvis", "lumbar",
                 "tibia_left_upper", "tibia_left_lower", "tibia_right_upper", "tibia_right_lower",
                 "femur", "knee", "foot_left", "foot_right", "seatbelt_force"]

    head = {
        "Resultant_Head_Angle_Velocity": {
            "code": "HEAD0000H3AVRD",
            "unit": "resultant [deg/s]"
        },
        "Head_Angle_Velocity_X": {
            "code": "HEAD0000H3AVXD",
            "unit": "angular velocity [deg/s]"
        },
        "Head_Angle_Velocity_Y": {
            "code": "HEAD0000H3AVYD",
            "unit": "angular velocity [deg/s]"
        },
        "Head_Angle_Velocity": {
            "code": "HEAD0000H3AVZD",
            "unit": "angular velocity [deg/s]"
        },
        "Resultant_Head_Acceleration": {
            "code": "HEAD0000H3ACRA",
            "unit": "resultant [g]"
        },
        "Head_Acceleration_X": {
            "code": "HEAD0000H3ACXA",
            "unit": "acceleration [g]"
        },
        "Head_Acceleration_Y": {
            "code": "HEAD0000H3ACYA",
            "unit": "acceleration [g]"
        },
        "Head_Acceleration_Z": {
            "code": "HEAD0000H3ACZA",
            "unit": "acceleration [g]"
        },
    }
    neck_upper = {
        "Resultant_Neck_Upper_Force": {
            "code": "NECKUP00H3FORA",
            "unit": "resultant [kN]"
        },
        "Neck_Upper_Force_X": {
            "code": "NECKUP00H3FOXA",
            "unit": "force [kN]"
        },
        "Neck_Upper_Force_X__Load_Duration_Time_": {
            "code": "NECKUPDNH3TIXA",
            "unit": "duration of loading [ms]"
        },
        "Neck_Upper_Force_X__Load_Duration_": {
            "code": "NECKUPDNH3FOXA",
            "unit": "force [kN]"
        },
        "Neck_Upper_Force_Y": {
            "code": "NECKUP00H3FOYA",
            "unit": "force [kN]"
        },
        "Neck_Upper_Force_Z": {
            "code": "NECKUP00H3FOZA",
            "unit": "force [kN]"
        },
        "Neck_Upper_Force_Z__Load_Duration_Time_": {
            "code": "NECKUPDNH3TIZA",
            "unit": "duration of loading [ms]"
        },
        "Neck_Upper_Force_Z__Load_Duration_": {
            "code": "NECKUPDNH3FOZA",
            "unit": "force [kN]"
        },
        "Resultant_Neck_Upper_Moment": {
            "code": "NECKUP00H3MORB",
            "unit": "resultant [Nm]"
        },
        "Neck_Upper_Moment_X": {
            "code": "NECKUP00H3MOXB",
            "unit": "moment [Nm]"
        },
        "Neck_Upper_Moment_X__Sum_": {
            "code": "NECKUPTOH3MOXB",
            "unit": "moment [Nm]"
        },
        "Neck_Upper_Moment_Y": {
            "code": "NECKUP00H3MOYB",
            "unit": "moment [Nm]"
        },
        "Neck_Upper_Moment_Y__Sum_": {
            "code": "NECKUPTOH3MOYB",
            "unit": "moment [Nm]"
        },
        "Neck_Upper_Moment_Y__Nce_": {
            "code": "NIJCIPCEH300YB",
            "unit": "Nij Criterion [1]"
        },
        "Neck_Upper_Moment_Y__Ncf_": {
            "code": "NIJCIPCFH300YB",
            "unit": "Nij Criterion [1]"
        },
        "Neck_Upper_Moment_Y__Nte_": {
            "code": "NIJCIPTEH300YB",
            "unit": "Nij Criterion [1]"
        },
        "Neck_Upper_Moment_Y__Ntf_": {
            "code": "NIJCIPTFH300YB",
            "unit": "Nij Criterion [1]"
        },
        "Neck_Upper_Moment_Z": {
            "code": "NECKUP00H3MOZB",
            "unit": "moment [Nm]"
        },
    }
    chest = {
        "Chest_Angle_Velocity_Y": {
            "code": "CHST0000H3AVYD",
            "unit": "angular velocity [deg/s]"
        },
        "Resultant_Chest_Acceleration": {
            "code": "CHST0000H3ACRC",
            "unit": "resultant [g]"
        },
        "Chest_Acceleration_X": {
            "code": "CHST0000H3ACXC",
            "unit": "acceleration [g]"
        },
        "Chest_Acceleration_Y": {
            "code": "CHST0000H3ACYC",
            "unit": "acceleration [g]"
        },
        "Chest_Acceleration_Z": {
            "code": "CHST0000H3ACZC",
            "unit": "acceleration [g]"
        },
        "Chest_Displacement_X": {
            "code": "CHST0003H3DSXB",
            "unit": "displacement [mm]"
        },
        "Chest_Displacement_X__Viscosity_": {
            "code": "VCCR0003H3VEXB",
            "unit": "viscosity [m/s]"
        },
    }
    pelvis = {
        "Resultant_Pelvis_Acceleration": {
            "code": "PELV0000H3ACRA",
            "unit": "resultant [g]"
        },
        "Pelvis_Acceleration_X": {
            "code": "PELV0000H3ACXA",
            "unit": "acceleration [g]"
        },
        "Pelvis_Acceleration_Y": {
            "code": "PELV0000H3ACYA",
            "unit": "acceleration [g]"
        },
        "Pelvis_Acceleration_Z": {
            "code": "PELV0000H3ACZA",
            "unit": "acceleration [g]"
        },
        "Resultant_Pelvis_Angle_Velocity": {
            "code": "PELV0000H3AVRD",
            "unit": "resultant [deg/s]"
        },
        "Pelvis_Angle_Velocity_X": {
            "code": "PELV0000H3AVXD",
            "unit": "angular velocity [deg/s]"
        },
        "Pelvis_Angle_Velocity_Y": {
            "code": "PELV0000H3AVYD",
            "unit": "angular velocity [deg/s]"
        },
        "Pelvis_Angle_Velocity_Z": {
            "code": "PELV0000H3AVZD",
            "unit": "angular velocity [deg/s]"
        },

    }
    lumbar = {
        "Resultant_Lumbar_Spine_Force": {
            "code": "LUSP0000H3FORB",
            "unit": "resultant [kN]"
        },
        "Lumbar_Spine_Force_X": {
            "code": "LUSP0000H3FOXB",
            "unit": "force [kN]"
        },
        "Lumbar_Spine_Force_Z": {
            "code": "LUSP0000H3FOZB",
            "unit": "force [kN]"
        },
        "Lumbar_Spine_Moent_Y": {
            "code": "LUSP0000H3MOYB",
            "unit": "moment [Nm]"
        },

    }
    tibia_left_upper = {
        "Tibia_Left_Upper_Force_X": {
            "code": "TIBILEUPH3FOXB",
            "unit": "force [kN]"
        },
        "Tibia_Left_Upper_Force_Z": {
            "code": "TIBILEUPH3FOZB",
            "unit": "force [kN]"
        },
        "Tibia_Left_Upper_Moment_X": {
            "code": "TIBILEUPH3MOXB",
            "unit": "moment [Nm]"
        },
        "Tibia_Left_Upper_Moment_Y": {
            "code": "TIBILEUPH3MOYB",
            "unit": "moment [Nm]"
        },
        "Tibia_Left_Upper_Moment_Y__FZ_Tibia_": {
            "code": "TIBILEUPH3FOZB",
            "unit": "force [kN]"
        },
        "Tibia_Left_Upper_Moment_Y__MR_Tibia_": {
            "code": "TIBILEUPH3MORB",
            "unit": "moment [Nm]"
        },
        "Tibia_Left_Upper_Moment_Y__Tibia_Index_": {
            "code": "TIINLEUPH3000B",
            "unit": "Tibia Index [1]"
        },
        "Tibia_Left_Upper_Moment_Y__TI_Fz_Ratio_": {
            "code": "TIRALUFOH300ZB",
            "unit": "Tibia Index [1]"
        },
        "Tibia_Left_Upper_Moment_Y__TI_MR_Ratio_": {
            "code": "TIRALUMOH300RB",
            "unit": "Tibia Index [1]"
        },
    }
    tibia_left_lower = {
        "Tibia_Left_Lower_Force_X": {
            "code": "TIBILELOH3FOXB",
            "unit": "force [kN]"
        },
        "Tibia_Left_Lower_Force_Z": {
            "code": "TIBILELOH3FOZB",
            "unit": "force [kN]"
        },
        "Tibia_Left_Lower_Moment_X": {
            "code": "TIBILELOH3MOXB",
            "unit": "moment [Nm]"
        },
        "Tibia_Left_Lower_Moment_Y": {
            "code": "TIBILELOH3MOYB",
            "unit": "moment [Nm]"
        },
        "Tibia_Left_Lower_Moment_Y__FZ_Tibia_": {
            "code": "TIBILELOH3FOZB",
            "unit": "force [kN]"
        },
        "Tibia_Left_Lower_Moment_Y__MR_Tibia_": {
            "code": "TIBILELOH3MORB",
            "unit": "moment [Nm]"
        },
        "Tibia_Left_Lower_Moment_Y__Tibia_Index_": {
            "code": "TIINLELOH3000B",
            "unit": "Tibia Index [1]"
        },
        "Tibia_Left_Lower_Moment_Y__TI_Fz_Ratio_": {
            "code": "TIRALLFOH300ZB",
            "unit": "Tibia Index [1]"
        },
        "Tibia_Left_Lower_Moment_Y__TI_MR_Ratio_": {
            "code": "TIRALLMOH300RB",
            "unit": "Tibia Index [1]"
        },
    }
    tibia_right_upper = {
        "Tibia_Right_Upper_Force_X": {
            "code": "TIBIRIUPH3FOXB",
            "unit": "force [kN]"
        },
        "Tibia_Right_Upper_Force_Z": {
            "code": "TIBIRIUPH3FOZB",
            "unit": "force [kN]"
        },
        "Tibia_Right_Upper_Moment_X": {
            "code": "TIBIRIUPH3MOXB",
            "unit": "moment [Nm]"
        },
        "Tibia_Right_Upper_Moment_Y": {
            "code": "TIBIRIUPH3MOYB",
            "unit": "moment [Nm]"
        },
        "Tibia_Right_Upper_Moment_Y__FZ_Tibia_": {
            "code": "TIBIRIUPH3FOZB",
            "unit": "force [kN]"
        },
        "Tibia_Right_Upper_Moment_Y__MR_Tibia_": {
            "code": "TIBIRIUPH3MORB",
            "unit": "moment [Nm]"
        },
        "Tibia_Right_Upper_Moment_Y__Tibia_Index_": {
            "code": "TIINRIUPH3000B",
            "unit": "Tibia Index [1]"
        },
        "Tibia_Right_Upper_Moment_Y__TI_Fz_Ratio_": {
            "code": "TIRARUFOH300ZB",
            "unit": "Tibia Index [1]"
        },
        "Tibia_Right_Upper_Moment_Y__TI_MR_Ratio_": {
            "code": "TIRARUMOH300RB",
            "unit": "Tibia Index [1]"
        },
    }
    tibia_right_lower = {
        "Tibia_Right_Lower_Force_Z": {
            "code": "TIBIRILOH3FOZB",
            "unit": "force [kN]"
        },
        "Tibia_Right_Lower_Force_X": {
            "code": "TIBIRILOH3FOXB",
            "unit": "force [kN]"
        },
        "Tibia_Right_Lower_Moment_Y": {
            "code": "TIBIRILOH3MOYB",
            "unit": "moment [Nm]"
        },
        "Tibia_Right_Lower_Moment_Y__FZ_Tibia_": {
            "code": "TIBIRILOH3FOZB",
            "unit": "force [kN]"
        },
        "Tibia_Right_Lower_Moment_Y__MR_Tibia_": {
            "code": "TIBIRILOH3MORB",
            "unit": "moment [Nm]"
        },
        "Tibia_Right_Lower_Moment_Y__Tibia_Index_": {
            "code": "TIINRILOH3000B",
            "unit": "Tibia Index [1]"
        },
        "Tibia_Right_Lower_Moment_Y__TI_Fz_Ratio_": {
            "code": "TIRARLFOH300ZB",
            "unit": "Tibia Index [1]"
        },
        "Tibia_Right_Lower_Moment_Y__TI_MR_Ratio_": {
            "code": "TIRARLMOH300RB",
            "unit": "Tibia Index [1]"
        },
        "Tibia_Right_Lower_Moment_X": {
            "code": "TIBIRILOH3MOXB",
            "unit": "moment [Nm]"
        },

    }
    femur = {
        "Femur_Left_Force_Z": {
            "code": "13FEMRLE00H3FOZB",
            "unit": "force [kN]"
        },
        "Femur_Right_Force_Z": {
            "code": "13FEMRRI00H3FOZB",
            "unit": "force [kN]"
        },
    }
    knee = {
        "Knee_Slider_Left_Displacement_X": {
            "code": "KNSLLE00H3DSXC",
            "unit": "displacement [mm]"
        },
        "Knee_Slider_Right_Displacement_X": {
            "code": "KNSLRI00H3DSXC",
            "unit": "displacement [mm]"
        },
    }
    foot_left = {
        "Resultant_Foot_Left_Acceleration": {
            "code": "FOOTLE00H3ACRC",
            "unit": "resultant [g]"
        },
        "Foot_Left_Acceleration_X": {
            "code": "FOOTLE00H3ACXC",
            "unit": "acceleration [g]"
        },
        "Foot_Left_Acceleration_Y": {
            "code": "FOOTLE00H3ACYC",
            "unit": "acceleration [g]"
        },
        "Foot_Left_Acceleration_Z": {
            "code": "FOOTLE00H3ACZC",
            "unit": "acceleration [g]"
        },

    }
    foot_right = {
        "Resultant_Foot_Right_Acceleration": {
            "code": "FOOTRI00H3ACRC",
            "unit": "resultant [g]"
        },
        "Foot_Right_Acceleration_X": {
            "code": "FOOTRI00H3ACXC",
            "unit": "acceleration [g]"
        },
        "Foot_Right_Acceleration_Y": {
            "code": "FOOTRI00H3ACYC",
            "unit": "acceleration [g]"
        },
        "Foot_Right_Acceleration_Z": {
            "code": "FOOTRI00H3ACZC",
            "unit": "acceleration [g]"
        },


    }
    seatbelt_force = {
        "SHO_TENSION_OTR": {
            "code": "SEBEFR00B3FO0D",
            "unit": "force [kN]"
        },
        "SHO_TENSION_INR": {
            "code": "SEBEFR00B4FO0D",
            "unit": "force [kN]"
        },
        "LAP_TENSION_OTR": {
            "code": "SEBEFR00B6FO0D",
            "unit": "force [kN]"
        }
    }


class H3_05(H3_50):
    __field__ = ["head", 'neck_upper', "chest", "pelvis", "iliac",
                 "femur",  "seatbelt_force", "seatbelt_reaction"]

    head = {
        "Resultant_Head_Acceleration": {
            "code": "HEAD0000HFACRA",
            "unit": "resultant [g]"
        },
        "Head_Acceleration_X": {
            "code": "HEAD0000HFACXA",
            "unit": "acceleration [g]"
        },
        "Head_Acceleration_Y": {
            "code": "HEAD0000HFACYA",
            "unit": "acceleration [g]"
        },
        "Head_Acceleration_Z": {
            "code": "HEAD0000HFACZA",
            "unit": "acceleration [g]"
        },
    }
    neck_upper = {
        "Resultant_Neck_Upper_Force": {
            "code": "NECKUP00HFFORA",
            "unit": "resultant [kN]"
        },
        "Neck_Upper_Force_X": {
            "code": "NECKUP00HFFOXA",
            "unit": "force [kN]"
        },
        "Neck_Upper_Force_X__Load_Duration_Time_": {
            "code": "NECKUPDAHFTIXA",
            "unit": "duration of loading [ms]"
        },
        "Neck_Upper_Force_X__Load_Duration_": {
            "code": "NECKUPDAHFFOXA",
            "unit": "force [kN]"
        },
        "Neck_Upper_Force_Y": {
            "code": "NECKUP00HFFOYA",
            "unit": "force [kN]"
        },
        "Neck_Upper_Force_Z": {
            "code": "NECKUP00HFFOZA",
            "unit": "force [kN]"
        },
        "Neck_Upper_Force_Z__Load_Duration_Time_": {
            "code": "NECKUPDNHFTIZA",
            "unit": "duration of loading [ms]"
        },
        "Neck_Upper_Force_Z__Load_Duration_": {
            "code": "NECKUPDNHFFOZA",
            "unit": "force [kN]"
        },
        "Resultant_Neck_Upper_Moment": {
            "code": "NECKUP00HFMORB",
            "unit": "resultant [Nm]"
        },
        "Neck_Upper_Moment_X": {
            "code": "NECKUP00HFMOXB",
            "unit": "moment [Nm]"
        },
        "Neck_Upper_Moment_X__Sum_": {
            "code": "NECKUPTOHFMOXB",
            "unit": "moment [Nm]"
        },
        "Neck_Upper_Moment_Y": {
            "code": "NECKUP00HFMOYB",
            "unit": "moment [Nm]"
        },
        "Neck_Upper_Moment_Y__Sum_": {
            "code": "NECKUPTOHFMOYB",
            "unit": "moment [Nm]"
        },
        "Neck_Upper_Moment_Y__Nce_": {
            "code": "NIJCIPCEHF00YB",
            "unit": "Nij Criterion [1]"
        },
        "Neck_Upper_Moment_Y__Ncf_": {
            "code": "NIJCIPCFHF00YB",
            "unit": "Nij Criterion [1]"
        },
        "Neck_Upper_Moment_Y__Nte_": {
            "code": "NIJCIPTEHF00YB",
            "unit": "Nij Criterion [1]"
        },
        "Neck_Upper_Moment_Y__Ntf_": {
            "code": "NIJCIPTFHF00YB",
            "unit": "Nij Criterion [1]"
        },
        "Neck_Upper_Moment_Z": {
            "code": "NECKUP00HFMOZB",
            "unit": "moment [Nm]"
        },
    }
    chest = {
        "Resultant_Chest_Acceleration": {
            "code": "CHST0000HFACRC",
            "unit": "resultant [g]"
        },
        "Chest_Acceleration_X": {
            "code": "CHST0000HFACXC",
            "unit": "acceleration [g]"
        },
        "Chest_Acceleration_Y": {
            "code": "CHST0000HFACYC",
            "unit": "acceleration [g]"
        },
        "Chest_Acceleration_Z": {
            "code": "CHST0000HFACZC",
            "unit": "acceleration [g]"
        },
        "Chest_Displacement_X": {
            "code": "CHST0000HFDSXB",
            "unit": "displacement [mm]"
        },
        "Chest_Displacement_X__Viscosity_": {
            "code": "VCCR0000HFVEXB",
            "unit": "viscosity [m/s]"
        },
    }
    pelvis = {
        "Resultant_Pelvis_Acceleration": {
            "code": "PELV0000HFACRB",
            "unit": "resultant [g]"
        },
        "Pelvis_Acceleration_X": {
            "code": "PELV0000HFACXB",
            "unit": "acceleration [g]"
        },
        "Pelvis_Acceleration_Y": {
            "code": "PELV0000HFACYB",
            "unit": "acceleration [g]"
        },
        "Pelvis_Acceleration_Z": {
            "code": "PELV0000HFACZB",
            "unit": "acceleration [g]"
        },
        "PELV0000HFVERB velocity": {
            "code": "PELV0000HFVERB",
            "unit": "velocity [m/s]"
        },
        "Pelvis_Angle_Velocity_Y": {
            "code": "PELV0000H3AVYD",
            "unit": "angular velocity [deg/s]"
        },
    }
    iliac = {
        "Iliac_Wing_Left_Force_X": {
            "code": "ILACLE00HFFOXC",
            "unit": "force [kN]"
        },
        "14ILACLE00HFFAXC,_2021-0092-FR-NISSAN-21-NCAP-100P,_CFC180,_Dev_1": {
            "code": "ILACLE00HFFAXC",
            "unit": "Force Rate [N/s]"
        },
        "Iliac_Wing_Left_Moment_Y": {
            "code": "ILACLE00HFMOYB",
            "unit": "moment [Nm]"
        },
        "Iliac_Wing_Right_Force_X": {
            "code": "ILACRI00HFFOXC",
            "unit": "force [kN]"
        },
        "14ILACRI00HFFAXC,_2021-0092-FR-NISSAN-21-NCAP-100P,_CFC180,_Dev_1": {
            "code": "ILACRI00HFFAXC",
            "unit": "Force Rate [N/s]"
        },
        "Iliac_Wing_Right_Moment_Y": {
            "code": "ILACRI00HFMOYB",
            "unit": "moment [Nm]"
        },

    }
    femur = {
        "Femur_Left_Force_Z": {
            "code": "FEMRLE00HFFOZB",
            "unit": "force [kN]"
        },
        "Femur_Left_Force_Z__Load_Duration_Time_": {
            "code": "FEMRLEDUHFTIZB",
            "unit": "duration of loading [ms]"
        },
        "Femur_Left_Force_Z__Load_Duration_": {
            "code": "FEMRLEDPHFFOZB",
            "unit": "force [kN]"
        },
        "Femur_Right_Force_Z": {
            "code": "FEMRRI00HFFOZB",
            "unit": "force [kN]"
        },
        "Femur_Right_Force_Z__Load_Duration_Time_": {
            "code": "FEMRRIDUHFTIZB",
            "unit": "duration of loading [ms]"
        },
        "Femur_Right_Force_Z__Load_Duration_": {
            "code": "FEMRRIDPHFFOZB",
            "unit": "force [kN]"
        },

    }
    seatbelt_force = {
        "FEMALE_SEAT_BELT_AT_Pos_B3": {
            "code": "SEBEFR00B3FO0D",
            "unit": "force [kN]"
        },
        "FEMALE_SEAT_BELT_AT_Pos_B6": {
            "code": "SEBEFR00B6FO0D",
            "unit": "force [kN]"
        }
    }
    seatbelt_reaction = {
        "Cu._FAMALE_SEAT_BELT_RETRACTOR_1": {
            "code": "SEBE01RETRCU0P",
            "unit": "current [A]"
        }
    }


class THOR(H3_50):

    __field__ = ["head", "neck_angle", 'neck_upper', 'neck_lower', "chest",
                 'abdomen', 'acetabulum', "clavicle", 'femur_left', 'femur_right', "iliac",
                 "pelvis", "T1", "T12", "T4", "sternum", "knee",
                 "tibia_left_lower", "tibia_left_upper", "tibia_right_upper", "tibia_right_lower",
                 "seatbelt_force", "seatbelt_reaction"]

    head = {
        "Resultant_Head_Acceleration": {
            "code": "HEAD0000T3ACRA",
            "unit": "resultant [g]"
        },
        "Head_Acceleration_X": {
            "code": "HEAD0000T3ACXA",
            "unit": "acceleration [g]"
        },
        "Head_Acceleration_Y": {
            "code": "HEAD0000T3ACYA",
            "unit": "acceleration [g]"
        },
        "Head_Acceleration_Z": {
            "code": "HEAD0000T3ACZA",
            "unit": "acceleration [g]"
        },
        "Resultant_Head_Angular_Veloctiy": {
            "code": "HEAD0000T3AVRD",
            "unit": "resultant [deg/s]"
        },
        "Head_Angular_Veloctiy_X": {
            "code": "HEAD0000T3AVXD",
            "unit": "angular velocity [deg/s]"
        },
        "Head_Angular_Veloctiy_Y": {
            "code": "HEAD0000T3AVYD",
            "unit": "angular velocity [deg/s]"
        },
        "Head_Angular_Veloctiy_Z": {
            "code": "HEAD0000T3AVZD",
            "unit": "angular velocity [deg/s]"
        },
        "Head_Frontal_Bone_Left_Force_X": {
            "code": "HEADUPLET3FOXA",
            "unit": "force [kN]"
        },
        "Head_Frontal_Bone_Right_Force_X": {
            "code": "HEADUPRIT3FOXA",
            "unit": "force [kN]"
        },
        "Head_Mandibula_Force_X": {
            "code": "HEADLO00T3FOXA",
            "unit": "force [kN]"
        },
        "Head_Maxilla_Left_Force_X": {
            "code": "HEADMILET3FOXA",
            "unit": "force [kN]"
        },
        "Head_Maxilla_Right_Force_X": {
            "code": "HEADMIRIT3FOXA",
            "unit": "force [kN]"
        },

    }
    neck_angle = {
        "Head/Neck_Angle_Y": {
            "code": "NECKUP00T3ANYD",
            "unit": "angle [deg]"
        },
    }
    neck_lower = {
        "Resultant_Lower_Neck_Force": {
            "code": "NECKLO00T3FORA",
            "unit": "resultant [kN]"
        },
        "Lower_Neck_Force_X": {
            "code": "NECKLO00T3FOXA",
            "unit": "force [kN]"
        },
        "Lower_Neck_Force_Y": {
            "code": "NECKLO00T3FOYA",
            "unit": "force [kN]"
        },
        "Lower_Neck_Force_Z": {
            "code": "NECKLO00T3FOZA",
            "unit": "force [kN]"
        },
        "Resultant_Lower_Neck_Moment": {
            "code": "NECKLO00T3MORB",
            "unit": "resultant [Nm]"
        },
        "Lower_Neck_Moment_X": {
            "code": "NECKLO00T3MOXB",
            "unit": "moment [Nm]"
        },
        "Lower_Neck_Moment_X__Sum_": {
            "code": "NECKLOTOT3MOXB",
            "unit": "moment [Nm]"
        },
        "Lower_Neck_Moment_Y": {
            "code": "NECKLO00T3MOYB",
            "unit": "moment [Nm]"
        },
        "Lower_Neck_Moment_Y__Sum_": {
            "code": "NECKLOTOT3MOYB",
            "unit": "moment [Nm]"
        },
        "Lower_Neck_Moment_Z": {
            "code": "NECKLO00T3MOZB",
            "unit": "moment [Nm]"
        },
        "Lower_Neck_Moment_Z__Sum_": {
            "code": "NECKLOTOT3MOZB",
            "unit": "moment [Nm]"
        },
        "Neck_Front_Cable_Force_Z": {
            "code": "NECKFR00T3FOZA",
            "unit": "force [kN]"
        },
        "Neck_Rear_Cable_Force_Z": {
            "code": "NECKRE00T3FOZA",
            "unit": "force [kN]"
        },
    }
    neck_upper = {
        "Resultant_Upper_Neck_Force": {
            "code": "NECKUP00T3FORA",
            "unit": "resultant [kN]"
        },
        "Upper_Neck_Force_X": {
            "code": "NECKUP00T3FOXA",
            "unit": "force [kN]"
        },
        "Upper_Neck_Force_Y": {
            "code": "NECKUP00T3FOYA",
            "unit": "force [kN]"
        },
        "Upper_Neck_Force_Z": {
            "code": "NECKUP00T3FOZA",
            "unit": "force [kN]"
        },
        "Resultant_Upper_Neck_Moment": {
            "code": "NECKUP00T3MORB",
            "unit": "resultant [Nm]"
        },
        "Upper_Neck_Moment_X": {
            "code": "NECKUP00T3MOXB",
            "unit": "moment [Nm]"
        },
        "Upper_Neck_Moment_X__Sum_": {
            "code": "NECKUPTOT3MOXB",
            "unit": "moment [Nm]"
        },
        "Upper_Neck_Moment_Y": {
            "code": "NECKUP00T3MOYB",
            "unit": "moment [Nm]"
        },
        "Upper_Neck_Moment_Y__Sum_": {
            "code": "NECKUPTOT3MOYB",
            "unit": "moment [Nm]"
        },
        "Upper_Neck_Moment_Y__Nce_": {
            "code": "NIJCIPCET300YB",
            "unit": "Nij Criterion [1]"
        },
        "Upper_Neck_Moment_Y__Ncf_": {
            "code": "NIJCIPCFT300YB",
            "unit": "Nij Criterion [1]"
        },
        "Upper_Neck_Moment_Y__Nte_": {
            "code": "NIJCIPTET300YB",
            "unit": "Nij Criterion [1]"
        },
        "Upper_Neck_Moment_Y__Ntf_": {
            "code": "NIJCIPTFT300YB",
            "unit": "Nij Criterion [1]"
        },
        "Upper_Neck_Moment_Z": {
            "code": "NECKUP00T3MOZB",
            "unit": "moment [Nm]"
        },
    }
    chest = {
        "Resultant_Chest_Left_Upper_Deflection_": {
            "code": "CHSTLEUPT3DSRC",
            "unit": "resultant [mm]"
        },
        "Resultant_Chest_Right_Upper_Deflection": {
            "code": "CHSTRIUPT3DSRC",
            "unit": "resultant [mm]"
        },
        "Resultant_Chest_Left_Lower_Deflection": {
            "code": "CHSTLELOT3DSRC",
            "unit": "resultant [mm]"
        },
        "Resultant_Chest_Right_Lower_Deflection": {
            "code": "CHSTRILOT3DSRC",
            "unit": "resultant [mm]"
        },

        "Chest_Left_Lower_Deflection_X": {
            "code": "CHSTLELOT3DC0C",
            "unit": "distance [mm]"
        },
        "Chest_Left_Lower_IR-TRACC_Rotation_Y": {
            "code": "CHSTLELOT3ANYC",
            "unit": "angle [deg]"
        },
        "Chest_Left_Lower_IR-TRACC_Rotation_Z": {
            "code": "CHSTLELOT3ANZC",
            "unit": "angle [deg]"
        },
        "Chest_Left_Upper_Deflection__X": {
            "code": "CHSTLEUPT3DC0C",
            "unit": "distance [mm]"
        },
        "Chest_Left_Upper_IR-TRACC_Rotation_Y": {
            "code": "CHSTLEUPT3ANYC",
            "unit": "angle [deg]"
        },
        "Chest_Left_Upper_IR-TRACC_Rotation_Z": {
            "code": "CHSTLEUPT3ANZC",
            "unit": "angle [deg]"
        },
        "Chest_Right_Lower_Deflection_X": {
            "code": "CHSTRILOT3DC0C",
            "unit": "distance [mm]"
        },
        "Chest_Right_Lower_IR-TRACC_Rotation_Y": {
            "code": "CHSTRILOT3ANYC",
            "unit": "angle [deg]"
        },
        "Chest_Right_Lower_IR-TRACC_Rotation_Z": {
            "code": "CHSTRILOT3ANZC",
            "unit": "angle [deg]"
        },
        "Chest_Right_Upper_Deflection_X": {
            "code": "CHSTRIUPT3DC0C",
            "unit": "distance [mm]"
        },
        "Chest_Right_Upper_IR-TRACC_Rotation_Y": {
            "code": "CHSTRIUPT3ANYC",
            "unit": "angle [deg]"
        },
        "Chest_Right_Upper_IR-TRACC_Rotation_Z": {
            "code": "CHSTRIUPT3ANZC",
            "unit": "angle [deg]"
        },
    }
    # 腹部
    abdomen = {
        "Resultant_Abdomen_Left_Deflection": {
            "code": "ABDOLE00T3DSRC",
                    "unit": "resultant [mm]"
        },
        "Resultant_Abdomen_Right_Deflection": {
            "code": "ABDORI00T3DSRC",
            "unit": "resultant [mm]"
        },
        "Abdomen_Left_Deflection_X": {
            "code": "ABDOLE00T3DC0C",
            "unit": "distance [mm]"
        },
        "Abdomen_Left_IR-TRACC_Rotation_Y": {
            "code": "ABDOLE00T3ANYC",
            "unit": "angle [deg]"
        },
        "Abdomen_Left_IR-TRACC_Rotation_Z": {
            "code": "ABDOLE00T3ANZC",
            "unit": "angle [deg]"
        },
        "Abdomen_Right_Deflection_X": {
            "code": "ABDORI00T3DC0C",
            "unit": "distance [mm]"
        },
        "Abdomen_Right_IR-TRACC_Rotation_Y": {
            "code": "ABDORI00T3ANYC",
            "unit": "angle [deg]"
        },
        "Abdomen_Right_IR-TRACC_Rotation_Z": {
            "code": "ABDORI00T3ANZC",
            "unit": "angle [deg]"
        },
        "Abdomen_Upper_Acceleration_X": {
            "code": "ABDOUP00T3ACXC",
            "unit": "acceleration [g]"
        },

    }
    # 髋臼
    acetabulum = {
        "Resultant_Acetabulum_Left_Force": {
            "code": "ACTBLE00T3FORB",
            "unit": "resultant [kN]"
        },
        "Acetabulum_Left_Force_X": {
            "code": "ACTBLE00T3FOXB",
            "unit": "force [kN]"
        },
        "Acetabulum_Left_Force_Y": {
            "code": "ACTBLE00T3FOYB",
            "unit": "force [kN]"
        },
        "Acetabulum_Left_Force_Z": {
            "code": "ACTBLE00T3FOZB",
            "unit": "force [kN]"
        },
        "Resultant_Acetabulum_Right_Force": {
            "code": "ACTBRI00T3FORB",
            "unit": "resultant [kN]"
        },
        "Acetabulum_Right_Force_X": {
            "code": "ACTBRI00T3FOYB",
            "unit": "force [kN]"
        },
        "Acetabulum_Right_Force_Z": {
            "code": "ACTBRI00T3FOZB",
            "unit": "force [kN]"
        },

    }
    # 锁骨
    clavicle = {
        "Clavicle_Left_Lateral_FX": {
            "code": "CLAVLEOUT3FOXA",
            "unit": "force [kN]"
        },
        "Clavicle_Left_Lateral_FZ": {
            "code": "CLAVLEOUT3FOZA",
            "unit": "force [kN]"
        },
        "Clavicle_Left_Medial_FX": {
            "code": "CLAVLEINT3FOXA",
            "unit": "force [kN]"
        },
        "Clavicle_Left_Medial_FZ": {
            "code": "CLAVLEINT3FOZA",
            "unit": "force [kN]"
        },
        "Clavicle_Right_Lateral_FX": {
            "code": "CLAVRIOUT3FOXA",
            "unit": "force [kN]"
        },
        "Clavicle_Right_Lateral_FZ": {
            "code": "CLAVRIOUT3FOZA",
            "unit": "force [kN]"
        },
        "Clavicle_Right_Medial__FZ": {
            "code": "CLAVRIINT3FOZA",
            "unit": "force [kN]"
        },
        "Clavicle_Right_Medial_FX": {
            "code": "CLAVRIINT3FOXA",
            "unit": "force [kN]"
        },
    }
    femur_left = {
        "Resultant_Femur_Left_Force": {
            "code": "FEMRLE00T3FORB",
            "unit": "resultant [kN]"
        },
        "Femur_Left_Force_X": {
            "code": "FEMRLE00T3FOXB",
            "unit": "force [kN]"
        },
        "Femur_Left_Force_Y": {
            "code": "FEMRLE00T3FOYB",
            "unit": "force [kN]"
        },
        "Femur_Left_Force_Z": {
            "code": "FEMRLE00T3FOZB",
            "unit": "force [kN]"
        },
        "Femur_Left_Force_Z__Load_Duration_Time_": {
            "code": "FEMRLEDUT3TIZB",
            "unit": "duration of loading [ms]"
        },
        "Femur_Left_Force_Z__Load_Duration_": {
            "code": "FEMRLEDPT3FOZB",
            "unit": "force [kN]"
        },
        "Femur_Left_Moment_X": {
            "code": "FEMRLE00T3MOXB",
            "unit": "moment [Nm]"
        },
        "Resultant_Femur_Left_Moment": {
            "code": "FEMRLE00T3MORB",
            "unit": "resultant [Nm]"
        },
        "Femur_Left_Moment_Y": {
            "code": "FEMRLE00T3MOYB",
            "unit": "moment [Nm]"
        },
        "Femur_Left_Moment_Z": {
            "code": "FEMRLE00T3MOZB",
            "unit": "moment [Nm]"
        },
    }
    femur_right = {
        "Resultant_Femur_Right_Force": {
            "code": "FEMRRI00T3FORB",
            "unit": "resultant [kN]"
        },
        "Femur_Right_Force_X": {
            "code": "FEMRRI00T3FOXB",
            "unit": "force [kN]"
        },
        "Femur_Right_Force_Y": {
            "code": "FEMRRI00T3FOYB",
            "unit": "force [kN]"
        },
        "Femur_Right_Force_Z": {
            "code": "FEMRRI00T3FOZB",
            "unit": "force [kN]"
        },
        "Femur_Right_Force_Z__Load_Duration_Time_": {
            "code": "FEMRRIDUT3TIZB",
            "unit": "duration of loading [ms]"
        },
        "Femur_Right_Force_Z__Load_Duration_": {
            "code": "FEMRRIDPT3FOZB",
            "unit": "force [kN]"
        },
        "Femur_Right_Moment_X": {
            "code": "FEMRRI00T3MOXB",
            "unit": "moment [Nm]"
        },
        "Resultant_Femur_Right_Moment": {
            "code": "FEMRRI00T3MORB",
            "unit": "resultant [Nm]"
        },
        "Femur_Right_Moment_Y": {
            "code": "FEMRRI00T3MOYB",
            "unit": "moment [Nm]"
        },
        "Femur_Right_Moment_Z": {
            "code": "FEMRRI00T3MOZB",
            "unit": "moment [Nm]"
        },
    }
    # 髂骨
    iliac = {
        "Iliac_Left_Force_X": {
            "code": "ILACLE00T3FOXB",
            "unit": "force [kN]"
        },
        "Iliac_Left_Moment_Y": {
            "code": "ILACLE00T3MOYB",
            "unit": "moment [Nm]"
        },
        "Iliac_Right_Force_X": {
            "code": "ILACRI00T3FOXB",
            "unit": "force [kN]"
        },
        "Iliac_Right_Moment_Y": {
            "code": "ILACRI00T3MOYB",
            "unit": "moment [Nm]"
        },
    }

    # 骨盆
    pelvis = {
        "Resultant_Pelvis_Acceleration": {
            "code": "PELV0000T3ACRA",
            "unit": "resultant [g]"
        },
        "Pelvis_Acceleration_X": {
            "code": "PELV0000T3ACXA",
            "unit": "acceleration [g]"
        },
        "Pelvis_Acceleration_Y": {
            "code": "PELV0000T3ACYA",
            "unit": "acceleration [g]"
        },
        "Pelvis_Acceleration_Z": {
            "code": "PELV0000T3ACZA",
            "unit": "acceleration [g]"
        },
        "Resultant_Pelvis_Angular_Velocity": {
            "code": "PELV0000T3AVRD",
            "unit": "resultant [deg/s]"
        },
        "Pelvis_Angular_Velocity_X": {
            "code": "PELV0000T3AVXD",
            "unit": "angular velocity [deg/s]"
        },
        "Pelvis_Angular_Velocity_Y": {
            "code": "PELV0000T3AVYD",
            "unit": "angular velocity [deg/s]"
        },
        "Pelvis_Angular_Velocity_Z": {
            "code": "PELV0000T3AVZD",
            "unit": "angular velocity [deg/s]"
        },
    }
    # 肋骨 T1T12T4
    T1 = {
        "Resultant_T1_Acceleration": {
            "code": "THSP0100T3ACRC",
            "unit": "resultant [g]"
        },
        "T1_X_Acceleration": {
            "code": "THSP0100T3ACXC",
            "unit": "acceleration [g]"
        },
        "T1_Y_Acceleration": {
            "code": "THSP0100T3ACYC",
            "unit": "acceleration [g]"
        },
        "T1_Z_Acceleration": {
            "code": "THSP0100T3ACZC",
            "unit": "acceleration [g]"
        },
    }
    T12 = {
        "Resultant_T12_Acceleration": {
            "code": "THSP1200T3ACRC",
            "unit": "resultant [g]"
        },
        "T12_Acceleration_X": {
            "code": "THSP1200T3ACXC",
            "unit": "acceleration [g]"
        },
        "T12_Acceleration_Y": {
            "code": "THSP1200T3ACYC",
            "unit": "acceleration [g]"
        },
        "T12_Acceleration_Z": {
            "code": "THSP1200T3ACZC",
            "unit": "acceleration [g]"
        },
        "Resultant_T12_Force": {
            "code": "THSP1200T3FORB",
            "unit": "resultant [kN]"
        },
        "T12_Force_X": {
            "code": "THSP1200T3FOXB",
            "unit": "force [kN]"
        },
        "T12_Force_Y": {
            "code": "THSP1200T3FOYB",
            "unit": "force [kN]"
        },
        "T12_Force_Z": {
            "code": "THSP1200T3FOZB",
            "unit": "force [kN]"
        },
        "T12_Moment_X": {
            "code": "THSP1200T3MOXB",
            "unit": "moment [Nm]"
        },
        "T12_Moment_Y": {
            "code": "THSP1200T3MOYB",
            "unit": "moment [Nm]"
        },
    }
    # T4 用于计算胸骨运动
    T4 = {

        "Resultant_T4_Acceleration": {
            "code": "THSP0400T3ACRC",
            "unit": "resultant [g]"
        },
        "T4_Acceleration_X": {
            "code": "THSP0400T3ACXC",
            "unit": "acceleration [g]"
        },
        "T4_Acceleration_Z": {
            "code": "THSP0400T3ACZC",
            "unit": "acceleration [g]"
        },
        "T4_Acceleration_Y": {
            "code": "THSP0400T3ACYC",
            "unit": "acceleration [g]"
        },
    }
    # 胸骨胸板
    sternum = {
        "Sternum_Middle_Acceleration_X": {
            "code": "STRNMI00T3ACXA",
            "unit": "acceleration [g]"
        },
    }
    knee = {
        "Knee_Slider_Left_Displacement_X": {
            "code": "KNSLLE00T3DSXC",
            "unit": "displacement [mm]"
        },
        "Knee_Slider_Right_Displacement_X": {
            "code": "KNSLRI00T3DSXC",
            "unit": "displacement [mm]"
        },
    }
    tibia_left_lower = {
        "Tibia_Left_Lower_Force_X": {
            "code": "TIBILELOT3FOXB",
            "unit": "force [kN]"
        },
        "Tibia_Left_Lower_Force_Z": {
            "code": "TIBILELOT3FOZB",
            "unit": "force [kN]"
        },
        "Tibia_Left_Lower_Moment_X": {
            "code": "TIBILELOT3MOXB",
            "unit": "moment [Nm]"
        },
        "Resultant_Tibia_Left_Lower_Moment": {
            "code": "TIBILELOT3MORB",
            "unit": "resultant [Nm]"
        },
        "Tibia_Left_Lower_Moment_Y": {
            "code": "TIBILELOT3MOYB",
            "unit": "moment [Nm]"
        },
        "Tibia_Left_Lower_Moment_Y__Sum_": {
            "code": "TIBILLTOT3MOYB",
            "unit": "moment [Nm]"
        },
        "Tibia_Left_Lower_Moment_Y__FZ_Tibia_": {
            "code": "TIBILELOT3FOZB",
            "unit": "force [kN]"
        },
        "Tibia_Left_Lower_Moment_Y__MR_Tibia_": {
            "code": "TIBILELOT3MORB",
            "unit": "moment [Nm]"
        },
        "Tibia_Left_Lower_Moment_Y__Tibia_Index_": {
            "code": "TIINLELOT3000B",
            "unit": "Tibia Index [1]"
        },
        "Tibia_Left_Lower_Moment_Y__TI_Fz_Ratio_": {
            "code": "TIRALLFOT300ZB",
            "unit": "Tibia Index [1]"
        },
        "Tibia_Left_Lower_Moment_Y__TI_MR_Ratio_": {
            "code": "TIRALLMOT300RB",
            "unit": "Tibia Index [1]"
        },
    }
    tibia_left_upper = {
        "Tibia_Left_Upper_Force_X": {
            "code": "TIBILEUPT3FOXB",
            "unit": "force [kN]"
        },
        "Tibia_Left_Upper_Force_Z": {
            "code": "TIBILEUPT3FOZB",
            "unit": "force [kN]"
        },
        "Tibia_Left_Upper_Moment_X": {
            "code": "TIBILEUPT3MOXB",
            "unit": "moment [Nm]"
        },
        "Resultant_Tibia_Left_Upper_Moment": {
            "code": "TIBILEUPT3MORB",
            "unit": "resultant [Nm]"
        },
        "Tibia_Left_Upper_Moment_Y": {
            "code": "TIBILEUPT3MOYB",
            "unit": "moment [Nm]"
        },
        "Tibia_Left_Upper_Moment_Y__Sum_": {
            "code": "TIBILUTOT3MOYB",
            "unit": "moment [Nm]"
        },
        "Tibia_Left_Upper_Moment_Y__FZ_Tibia_": {
            "code": "TIBILEUPT3FOZB",
            "unit": "force [kN]"
        },
        "Tibia_Left_Upper_Moment_Y__MR_Tibia_": {
            "code": "TIBILEUPT3MORB",
            "unit": "moment [Nm]"
        },
        "Tibia_Left_Upper_Moment_Y__Tibia_Index_": {
            "code": "TIINLEUPT3000B",
            "unit": "Tibia Index [1]"
        },
        "Tibia_Left_Upper_Moment_Y__TI_Fz_Ratio_": {
            "code": "TIRALUFOT300ZB",
            "unit": "Tibia Index [1]"
        },
        "Tibia_Left_Upper_Moment_Y__TI_MR_Ratio_": {
            "code": "TIRALUMOT300RB",
            "unit": "Tibia Index [1]"
        },
    }
    tibia_right_upper = {
        "Tibia_Right_Upper_Force_X": {
            "code": "TIBIRIUPT3FOXB",
            "unit": "force [kN]"
        },
        "Tibia_Right_Upper_Force_Z": {
            "code": "TIBIRIUPT3FOZB",
            "unit": "force [kN]"
        },
        "Tibia_Right_Upper_Moment_X": {
            "code": "TIBIRIUPT3MOXB",
            "unit": "moment [Nm]"
        },
        "Resultant_Tibia_Right_Upper_Moment": {
            "code": "TIBIRIUPT3MORB",
            "unit": "resultant [Nm]"
        },
        "Tibia_Right_Upper_Moment_Y": {
            "code": "TIBIRIUPT3MOYB",
            "unit": "moment [Nm]"
        },
        "Tibia_Right_Upper_Moment_Y__Sum_": {
            "code": "TIBIRUTOT3MOYB",
            "unit": "moment [Nm]"
        },
        "Tibia_Right_Upper_Moment_Y__FZ_Tibia_": {
            "code": "TIBIRIUPT3FOZB",
            "unit": "force [kN]"
        },
        "Tibia_Right_Upper_Moment_Y__MR_Tibia_": {
            "code": "TIBIRIUPT3MORB",
            "unit": "moment [Nm]"
        },
        "Tibia_Right_Upper_Moment_Y__Tibia_Index_": {
            "code": "TIINRIUPT3000B",
            "unit": "Tibia Index [1]"
        },
        "Tibia_Right_Upper_Moment_Y__TI_Fz_Ratio_": {
            "code": "TIRARUFOT300ZB",
            "unit": "Tibia Index [1]"
        },
        "Tibia_Right_Upper_Moment_Y__TI_MR_Ratio_": {
            "code": "TIRARUMOT300RB",
            "unit": "Tibia Index [1]"
        },
    }
    tibia_right_lower = {
        "Tibia_Right_Lower_Force_X": {
            "code": "TIBIRILOT3FOXB",
            "unit": "force [kN]"
        },
        "Tibia_Right_Lower_Force_Z": {
            "code": "TIBIRILOT3FOZB",
            "unit": "force [kN]"
        },
        "Tibia_Right_Lower_Moment_X": {
            "code": "TIBIRILOT3MOXB",
            "unit": "moment [Nm]"
        },
        "Resultant_Tibia_Right_Lower_Moment": {
            "code": "TIBIRILOT3MORB",
            "unit": "resultant [Nm]"
        },
        "Tibia_Right_Lower_Moment_Y": {
            "code": "TIBIRILOT3MOYB",
            "unit": "moment [Nm]"
        },
        "Tibia_Right_Lower_Moment_Y__Sum_": {
            "code": "TIBIRLTOT3MOYB",
            "unit": "moment [Nm]"
        },
        "Tibia_Right_Lower_Moment_Y__FZ_Tibia_": {
            "code": "TIBIRILOT3FOZB",
            "unit": "force [kN]"
        },
        "Tibia_Right_Lower_Moment_Y__MR_Tibia_": {
            "code": "TIBIRILOT3MORB",
            "unit": "moment [Nm]"
        },
        "Tibia_Right_Lower_Moment_Y__Tibia_Index_": {
            "code": "TIINRILOT3000B",
            "unit": "Tibia Index [1]"
        },
        "Tibia_Right_Lower_Moment_Y__TI_Fz_Ratio_": {
            "code": "TIRARLFOT300ZB",
            "unit": "Tibia Index [1]"
        },
        "Tibia_Right_Lower_Moment_Y__TI_MR_Ratio_": {
            "code": "TIRARLMOT300RB",
            "unit": "Tibia Index [1]"
        },
    }
    seatbelt_force = {
        "SEAT_BELT_AT_Pos_B3": {
            "code": "SEBEFR00B3FO0D",
            "unit": "force [kN]"
        },
        "SEAT_BELT_AT_Pos_B4": {
            "code": "SEBEFR00B4FO0D",
            "unit": "force [kN]"
        },
        "SEAT_BELT_AT_Pos_B6": {
            "code": "SEBEFR00B6FO0D",
            "unit": "force [kN]"
        },
    }
    seatbelt_reaction = {
        "Cu_SEAT_BELT_RETRACTOR_1": {
            "code": "SEBE01RETRCU0P",
            "unit": "current [A]"
        },
    }


class Q3(Base_Dummy):
    __field__ = ["head", "neck_upper", "chest"]
    head = {
        "Resultant_Head_Acceleration": {
            "code": "HEAD0000Q3ACRA",
            "unit": "resultant [g]"
        },
        "Head_Acceleration_X": {
            "code": "HEAD0000Q3ACXA",
            "unit": "acceleration [g]"
        },
        "Head_Acceleration_Y": {
            "code": "HEAD0000Q3ACYA",
            "unit": "acceleration [g]"
        },
        "Head_Acceleration_Z": {
            "code": "HEAD0000Q3ACZA",
            "unit": "acceleration [g]"
        },
    }
    neck_upper = {
        "Resultant_Neck_Upper_Force": {
            "code": "NECKUP00Q3FORA",
            "unit": "resultant [kN]"
        },
        "Neck_Upper_Force_X": {
            "code": "NECKUP00Q3FOXA",
            "unit": "force [kN]"
        },
        "Neck_Upper_Force_Y": {
            "code": "NECKUP00Q3FOYA",
            "unit": "force [kN]"
        },
        "Neck_Upper_Force_Z": {
            "code": "NECKUP00Q3FOZA",
            "unit": "force [kN]"
        },
        "Resultant_Neck_Upper_Moment": {
            "code": "NECKUP00Q3MORB",
            "unit": "resultant [Nm]"
        },
        "Neck_Upper_Moment_X": {
            "code": "NECKUP00Q3MOXB",
            "unit": "moment [Nm]"
        },
        "Neck_Upper_Moment_X__Sum_": {
            "code": "NECKUP00Q3MOXB",
            "unit": "moment [Nm]"
        },
        "Neck_Upper_Moment_Y": {
            "code": "NECKUP00Q3MOYB",
            "unit": "moment [Nm]"
        },
        "Neck_Upper_Moment_Y__Sum_": {
            "code": "NECKUP00Q3MOYB",
            "unit": "moment [Nm]"
        },
        "Neck_Upper_Moment_Y__Nce_": {
            "code": "NIJCOPCEQ300YB",
            "unit": "Nij Criterion [1]"
        },
        "Neck_Upper_Moment_Y__Ncf_": {
            "code": "NIJCOPCFQ300YB",
            "unit": "Nij Criterion [1]"
        },
        "Neck_Upper_Moment_Y__Nte_": {
            "code": "NIJCOPTEQ300YB",
            "unit": "Nij Criterion [1]"
        },
        "Neck_Upper_Moment_Y__Ntf_": {
            "code": "NIJCOPTFQ300YB",
            "unit": "Nij Criterion [1]"
        },
        "Neck_Upper_Moment_Z": {
            "code": "NECKUP00Q3MOZB",
            "unit": "moment [Nm]"
        },
    }
    chest = {
        "Resultant_Chest_Acceleration": {
            "code": "THSP0000Q3ACRC",
            "unit": "resultant [g]"
        },
        "Chest_Acceleration_X": {
            "code": "THSP0000Q3ACXC",
            "unit": "acceleration [g]"
        },
        "Chest_Acceleration_Y": {
            "code": "THSP0000Q3ACYC",
            "unit": "acceleration [g]"
        },
        "Chest_Acceleration_Z": {
            "code": "THSP0000Q3ACZC",
            "unit": "acceleration [g]"
        },
        "Chest_Upper_IRTRACC_Displacement": {
            "code": "CHST0000Q3DSXC",
            "unit": "displacement [mm]"
        },
        "Chest_Upper_IRTRACC_Displacement__Viscosity_": {
            "code": "VCCR0000Q3VEXC",
            "unit": "viscosity [m/s]"
        },
    }


class Q10(Base_Dummy):
    __field__ = ["head","neck_upper","chest","lumbar","pelvis","abdomen","seatbelt_force"]
    head = {
        "Resultant_Head_Acceleration": {
            "code": "HEAD0000QAACRA",
            "unit": "resultant [g]"
        },
        "Head_Acceleration_X": {
            "code": "HEAD0000QAACXA",
            "unit": "acceleration [g]"
        },
        "Head_Acceleration_Y": {
            "code": "HEAD0000QAACYA",
            "unit": "acceleration [g]"
        },
        "Head_Acceleration_Z": {
            "code": "HEAD0000QAACZA",
            "unit": "acceleration [g]"
        },
        "Head_AV_Y": {
            "code": "HEAD0000QAAVYD",
            "unit": "angular velocity [deg/s]"
        },
    }
    neck_upper = {
        "Resultant_Neck_Upper_Force": {
            "code": "NECKUP00QAFORA",
            "unit": "resultant [kN]"
        },
        "Neck_Upper_Force_X": {
            "code": "NECKUP00QAFOXA",
            "unit": "force [kN]"
        },
        "Neck_Upper_Force_Y": {
            "code": "NECKUP00QAFOYA",
            "unit": "force [kN]"
        },
        "Neck_Upper_Force_Z": {
            "code": "NECKUP00QAFOZA",
            "unit": "force [kN]"
        },
        "Resultant_Neck_Upper_Moment": {
            "code": "NECKUP00QAMORB",
            "unit": "resultant [Nm]"
        },
        "Neck_Upper_Moment_X": {
            "code": "NECKUP00QAMOXB",
            "unit": "moment [Nm]"
        },
        "Neck_Upper_Moment_X__Sum_": {
            "code": "NECKUP00QAMOXB",
            "unit": "moment [Nm]"
        },
        "Neck_Upper_Moment_Y": {
            "code": "NECKUP00QAMOYB",
            "unit": "moment [Nm]"
        },
        "Neck_Upper_Moment_Y__Sum_": {
            "code": "NECKUP00QAMOYB",
            "unit": "moment [Nm]"
        },
        "Neck_Upper_Moment_Z": {
            "code": "NECKUP00QAMOZB",
            "unit": "moment [Nm]"
        },
    }
    chest = {
        "Resultant_Chest_Acceleration": {
            "code": "THSP0400QAACRC",
            "unit": "resultant [g]"
        },
        "Chest_Acceleration_X": {
            "code": "THSP0400QAACXC",
            "unit": "acceleration [g]"
        },
        "Chest_Acceleration_Y": {
            "code": "THSP0400QAACYC",
            "unit": "acceleration [g]"
        },
        "Chest_Acceleration_Z": {
            "code": "THSP0400QAACZC",
            "unit": "acceleration [g]"
        },
        "Chest_Upper_IRTRACC_Distance": {
            "code": "CHSTUP00QADC0C",
            "unit": "distance [mm]"
        },
        "Chest_Upper_IRTRACC_Angle": {
            "code": "CHSTUP00QAANZC",
            "unit": "angle [deg]"
        },
        "Chest_Lower_IRTRACC_Distance": {
            "code": "CHSTLO00QADC0C",
            "unit": "distance [mm]"
        },
        "Chest_Lower_IRTRACC_Angle": {
            "code": "CHSTLO00QAANZC",
            "unit": "angle [deg]"
        },
        "Chest_AV_Y": {
            "code": "THSP0400QAAVYD",
            "unit": "angular velocity [deg/s]"
        },
        "Chest_Upper_IRTRACC_Distance__Viscosity_": {
            "code": "VCCRUP00QAVEXC",
            "unit": "viscosity [m/s]"
        },
        "Chest_Lower_IRTRACC_Distance__Viscosity_": {
            "code": "VCCRLO00QAVEXC",
            "unit": "viscosity [m/s]"
        }
    }
    lumbar = {
        "Resultant_Lumbar_Spine_force": {
            "code": "LUSP0000QAFORA",
            "unit": "resultant [kN]"
        },
        "Lumbar_Spine_force_X": {
            "code": "LUSP0000QAFOXA",
            "unit": "force [kN]"
        },
        "Lumbar_Spine_force_Y": {
            "code": "LUSP0000QAFOYA",
            "unit": "force [kN]"
        },
        "Lumbar_Spine_force_Z": {
            "code": "LUSP0000QAFOZA",
            "unit": "force [kN]"
        },
        "Resultant_Lumbar_Spine_Moment": {
            "code": "LUSP0000QAMORB",
            "unit": "resultant [Nm]"
        },
        "Lumbar_Spine_Moment_X": {
            "code": "LUSP0000QAMOXB",
            "unit": "moment [Nm]"
        },
        "Lumbar_Spine_Moment_Y": {
            "code": "LUSP0000QAMOYB",
            "unit": "moment [Nm]"
        },
        "Lumbar_Spine_Moment_Z": {
            "code": "LUSP0000QAMOZB",
            "unit": "moment [Nm]"
        },
    }
    pelvis = {

        "Resultant_Pelvis_Acceleration": {
            "code": "PELV0000QAACRC",
            "unit": "resultant [g]"
        },
        "Pelvis_Acceleration_X": {
            "code": "PELV0000QAACXC",
            "unit": "acceleration [g]"
        },
        "Pelvis_Acceleration_Y": {
            "code": "PELV0000QAACYC",
            "unit": "acceleration [g]"
        },
        "Pelvis_Acceleration_Z": {
            "code": "PELV0000QAACZC",
            "unit": "acceleration [g]"
        },
        "Pelvis_AV_Y": {
            "code": "PELV0000QAAVYD",
            "unit": "angular velocity [deg/s]"
        },
    }
    # 腹部
    abdomen = {
        "Abdomen_Pressure_Left": {
            "code": "ABDOLE00QAPR0C",
            "unit": "pressure [Pa]"
        },
        "Abdomen_Pressure_Right": {
            "code": "ABDORI00QAPR0C",
            "unit": "pressure [Pa]"
        },
    }
    seatbelt_force = {
        "CHILD_SEAT_BELT_AT_Pos_B6": {
            "code": "SEBE0000B6FO0D",
            "unit": "force [kN]"
        },

    }
