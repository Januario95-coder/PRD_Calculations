IPRD_3_CHOICES = [
    ('convention_spring_loaded', 'Convention Spring-Loaded'),
    ('balanced_bellows', 'Balanced Bellows'),
    ('pilot_operated', 'Pilot Operated'),
    # ('prv_with_rupture_disk', 'PRV with Rupture Disk'),
    ('Rupture_disk_only', 'Rupture Disk Only')
]

IPRD_4_CHOICES = [
    ('no', 'No'),
    ('yes', 'Yes')
]

IPRD_6_CHOICES = [
    ('mild', 'Mild'),
    ('moderate', 'Moderate'),
    ('severe', 'Severe')
]

IPRD_7_CHOICES = [
    ('atmosphere', 'Atmosphere'),
    ('flare', 'Flare'),
    ('closed_process', 'Closed Process')
]

degree_sign = u"\N{DEGREE SIGN}"
IPRD_8_CHOICES = [
    (f'99.33 {degree_sign}C < T < 260 {degree_sign}C', f'Operating temperatures 99.33 {degree_sign}C < T < 260 {degree_sign}C'),
    (f'> 260 {degree_sign}C', f'Operating temperature > 260 {degree_sign}C'),
    ('>_90%_spring-loaded_or_>_95%_pilot-operated', 'Operating ratio > 90%\ for spring-loaded PRVs or > 95% for pilot operated'),
    ('installed_piping_vibration', 'Installed piping vibration'),
    ('pulsating_or_cyclical_service', 'Pulsating or cyclical service such as downstream of positive displacement rotating equipment'),
    ('history_of_excessive_actuation', 'History of excessive actuation in service (greater than 5 times per year'),
    ('history_of_chatter', 'History of chatter')
]

IPRD_9_CHOICES = [
    ('no', 'No'),
    ('yes', 'Yes')
]

IPRD_11_CHOICES = [
    ('none', 'None'),
    ('pass', 'Pass'),
    ('fail', 'Fail')
]

IPRD_12_CHOICES = [
    ('none', 'None'),
    ('leak', 'Leak'),
    ('no_leak', 'No Leak')
]

IPRD_13_CHOICES = [
    ('none', 'None'),
    ('highly_effective', 'Highly Effective'),
    ('usually_effective', 'Usually Effective'),
    ('faily_effective', 'Faily Effective'),
    ('highly_ineffective', 'Ineffective')
]

IPRD_14_CHOICES = [
    ('none', 'None'),
    ('yes', 'Yes'),
    ('no', 'No')
]

IPRD_15_CHOICES = [
    ('none', 'None'),
    ('yes', 'Yes'),
    ('no', 'No')
]

IPRD_16_CHOICES = [
    ('fire', '1. Fire'),
    ('loss_of_cooling_water', '2. Loss of cooling water utility'),
    ('electrical_power_supply_failure', '3. Electrical power supply failure'),
    ('blockage_discharge_with_admin_controls', '4. Blockage discharge with administrative controls in place'),
    ('blockage_discharge_without_admin_controls', '5. Blockage discharge without administrative controls'),
    ('control_valve_failure_initiating_event_is_same_direction_as_cv', '6. Control valve failure, initiating event is same direction as CV normal fail position (i.e. fail safe)'),
    ('control_valve_failure_initiating_event_is_opposite_direction_as_cv', '7. Control valve failure, initiating event is opposite direction as CV normal fail posiion (i.e. fail opposite)'),
    ('runaway_chemical_reaction', '8. Runaway chemical reaction'),
    ('heat_exchanger_tube_rupture', '9. Heat exchanger tube rupture'),
    ('tower_p/a_or_reflux_pump_failures', '10. Tower P/A or reflux pump failures'),
    ('thermal_relief_with_admini_controls', '11. Thermal relief with administrative controls in place'),
    ('thermal_relief_without_admin_controls', '12. Thermal relief without administrative controls'),
    ('liquid_overfilling_with_admin_controls', '13. Liquid overfilling with administrative controls in place'),
    ('liquid_overfilling_without_admin_controls', '14. Liquid overfilling without administrative controls')
]


IPRD_18_CHOICES = [
    ('yes', 'Yes'),
    ('no', 'No')
]

IPRD_19_CHOICES = [
    ('none', 'None'),
    ('minimal', 'Minimal'),
    ('minor', 'Minor'),
    ('moderate', 'Moderate'),
    ('severe', 'Severe')
]

IPRD_22_CHOICES = [
    ('yes', 'Yes'),
    ('no', 'No')
]

IPRD_30_CHOICES = [
    ('no', 'No'),
    ('yes', 'Yes')
]

