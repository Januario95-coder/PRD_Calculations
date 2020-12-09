

n_def = {
    'fuild_severity': {
        'mild': {
            'convention_spring_loaded': 50.5,
            'balanced_bellows': 50.5,
            'pilot_operated': 33.7,
            'Rupture_disk_only': 50.5
        },
        'moderate': {
            'convention_spring_loaded': 23.9,
            'balanced_bellows': 23.9,
            'pilot_operated': 8.0,
            'Rupture_disk_only': 50.5
        },
        'severe': {
            'convention_spring_loaded': 17.6,
            'balanced_bellows': 17.6,
            'pilot_operated': 3.5,
            'Rupture_disk_only': 50.5
        }
    }
}

def Fc_POD(val1, val2):
    if ((val1 == 'convention_spring_loaded' and
        val2 == 'flare') or
        (val2 == 'closed_process')):
        return 0.75
    else:
        return 1.0


def Fs_POL(iprd_3, iprd_4):
    fs_value = ''
    if ((iprd_3 == 'convention_spring_loaded' or
        iprd_3 == 'balanced_bellows') and
        (iprd_4 == 'yes')):
        fs_value = 1.25
    else:
        fs_value = 1

    return fs_value



CF = {
    'Inspection_Result': {
        'pass': {
            'highly_ineffective': 0,
            'faily_effective': 0.5,
            'usually_effective': 0.70,
            'highly_effective': 0.9
        },
        'fail': {
            'highly_ineffective': 0,
            'faily_effective': 0.70,
            'usually_effective': 0.95,
            'highly_effective': 0.95
        },
        'leak': {
            'highly_ineffective': 0,
            'faily_effective': 0.70,
            'usually_effective': 0.95,
            'highly_effective': 0.95
        },
        'no_leak': {
            'highly_ineffective': 0,
            'faily_effective': 0.5,
            'usually_effective': 0.70,
            'highly_effective': 0.9
        },
    }
}


EF_j = {
    'fire': 0.0040,
    'loss_of_cooling_water': 0.10,
    'electrical_power_supply_failure': 0.080,
    'blockage_discharge_with_admin_controls': 0.010,
    'blockage_discharge_without_admin_controls': 0.10,
    'control_valve_failure_initiating_event_is_same_direction_as_cv': 0.10,
    'control_valve_failure_initiating_event_is_opposite_direction_as_cv': 0.020,
    'runaway_chemical_reaction': 1.0,
    'heat_exchanger_tube_rupture': 0.0010,
    'tower_p/a_or_reflux_pump_failures': 0.2,
    'thermal_relief_with_admini_controls': 0.010,
    'thermal_relief_without_admin_controls': 0.10,
    'liquid_overfilling_with_admin_controls': 0.010,
    'liquid_overfilling_without_admin_controls': 0.10,
}

DDRF_j = {
    'fire': 0.10,
    'loss_of_cooling_water': 1.0,
    'electrical_power_supply_failure': 1.0,
    'blockage_discharge_with_admin_controls': 1.0,
    'blockage_discharge_without_admin_controls': 1.0,
    'control_valve_failure_initiating_event_is_same_direction_as_cv': 1.0,
    'control_valve_failure_initiating_event_is_opposite_direction_as_cv': 1.0,
    'runaway_chemical_reaction': 1.0,
    'heat_exchanger_tube_rupture': 1.0,
    'tower_p/a_or_reflux_pump_failures': 1.0,
    'thermal_relief_with_admini_controls': 1.0,
    'thermal_relief_without_admin_controls': 1.0,
    'liquid_overfilling_with_admin_controls': 0.10,
    'liquid_overfilling_without_admin_controls': 0.10,
}


DF_Class = {
    'none': 1,
    'minimal': 20,
    'minor': 200,
    'moderate': 750,
    'severe': 2000
}





n_def_pol = {
    'fuild_severity': {
        'mild': {
            'convention_spring_loaded': 17.5,
            'balanced_bellows': 16.0,
            'pilot_operated': 17.5,
            'Rupture_disk_only': 17.5
        },
        'moderate': {
            'convention_spring_loaded': 15.5,
            'balanced_bellows': 14.0,
            'pilot_operated': 15.5,
            'Rupture_disk_only': 17.5
        },
        'severe': {
            'convention_spring_loaded': 13.1,
            'balanced_bellows': 11.5,
            'pilot_operated': 13.1,
            'Rupture_disk_only': 17.5
        }
    }
}





degree_sign = u"\N{DEGREE SIGN}"

F_env_POD = {
    f'99.33 {degree_sign}C < T < 260 {degree_sign}C': 1.0,
    f'> 260 {degree_sign}C': 1.0,
    '>_90%_spring-loaded_or_>_95%_pilot-operated': 1.0,
    'installed_piping_vibration': 1.0,
    'pulsating_or_cyclical_service': 1.0,
    'history_of_excessive_actuation': 0.5,
    'history_of_chatter': 0.5
}

F_env_POL = {
    f'99.33 {degree_sign}C < T < 260 {degree_sign}C': 0.8,
    f'> 260 {degree_sign}C': 0.6,
    '>_90%_spring-loaded_or_>_95%_pilot-operated': 0.5,
    'installed_piping_vibration': 0.8,
    'pulsating_or_cyclical_service': 0.8,
    'history_of_excessive_actuation': 0.5,
    'history_of_chatter': 0.5
}


def D_mild(prd_inlet_size, PRD_Discharge_Location):
    data = 0
    if (prd_inlet_size <= 3/4):
        if (PRD_Discharge_Location == 'flare' or
            PRD_Discharge_Location == 'closed_process'):
            data = 60
        elif (PRD_Discharge_Location == 'atmosphere'):
            data = 8
    elif (3/4 < prd_inlet_size <= 1.5):
        if (PRD_Discharge_Location == 'flare' or
            PRD_Discharge_Location == 'closed_process'):
            data = 30
        elif (PRD_Discharge_Location == 'atmosphere'):
            data = 4
    elif (1.5 < prd_inlet_size <= 3):
        if (PRD_Discharge_Location == 'flare' or
            PRD_Discharge_Location == 'closed_process'):
            data = 15
        elif (PRD_Discharge_Location == 'atmosphere'):
            data = 2
    elif (3 < prd_inlet_size <= 6):
        if (PRD_Discharge_Location == 'flare' or
            PRD_Discharge_Location == 'closed_process'):
            data = 7
        elif (PRD_Discharge_Location == 'atmosphere'):
            data = 1
    elif prd_inlet_size > 6:
        if (PRD_Discharge_Location == 'flare' or
            PRD_Discharge_Location == 'closed_process'):
            data = 2
        elif (PRD_Discharge_Location == 'atmosphere'):
            data = 0.33
    return data


def Fr(PRD_Discharge_Location):
    value = 0
    if PRD_Discharge_Location == 'flare':
        value = 0.5
    elif PRD_Discharge_Location == 'closed_process':
        value = 0
    elif PRD_Discharge_Location == 'atmosphere':
        value = 1.0

    return value



def C_env(PRD_Discharge_Location,
          Environmental_clean_up_costs):
    value = 0
    if (PRD_Discharge_Location == 'flare' or
        PRD_Discharge_Location == 'atmosphere'):
        value = Environmental_clean_up_costs
    elif PRD_Discharge_Location == 'closed_process':
        value = 0

    return value


def C_sd(PRD_leakage_can_be_tolered,
         Cost_of_shutdown):
    value = 0
    if PRD_leakage_can_be_tolered == 'no':
        value = Cost_of_shutdown
    elif PRD_leakage_can_be_tolered == 'yes':
        value = 0

    return value



def F_set_formula(Type_of_PRD, P_set, P_s):
    result = 1
    if Type_of_PRD == 'pilot_operated':
        min_val = min(0.95, (float(P_s)/float(P_set)))
        result = 1 - ((0.95 - min_val) / 0.95)
    elif Type_of_PRD == 'Rupture_disk_only':
        result = 1
    elif (Type_of_PRD == 'convention_spring_loaded' or
             Type_of_PRD == 'balanced_bellows'):
        min_val = min(0.90, (float(P_s)/float(P_set)))
        result = 1 - ((0.90 - min_val) / 0.90)

    return result
