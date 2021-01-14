from django.shortcuts import (
    render, redirect,
    get_object_or_404
)
from django.contrib import messages
from django.contrib.auth import (
    authenticate,
    login,
    logout
)
from django.contrib.auth.decorators import login_required
from .forms import (
    LoginForm,
    GeneralInformationForm,
    PRD_InspectionForm,
    ConsequencesOfFailureInputDataForm,
    Consequences0fFailureOfLeakageForm,
    ApplicableOverpressureDemandCaseForm,
    Prd_InspectionHistoryForm
)
from .models import (
    GeneralInformation,
    Prd_InspectionHistory,
    ApplicableOverpressureDemandCase
)
import math
import csv
from datetime import datetime
import datetime as dt

from .Table_Ref import (
    # Values Reference for POD
    n_def, Fc_POD, F_env_POD, CF, EF_j, DDRF_j,
    DF_Class,

    # Values Reference for POL
    n_def_pol, Fs_POL, F_env_POL, D_mild, Fr, C_env,
    C_sd, F_set_formula
)


def login_page(request):
    form = LoginForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back {username}')
                return redirect('/prd/create_prd/')
            else:
                print("Wrong login credentails")
    else:
        form = LoginForm()

    return render(request,
            'webapp/login.html',
            {'form': form})


def logout_page(request):
  logout(request)
  return redirect('/prd/login/')


@login_required(login_url='/prd/login/')
def main_page(request):
    return render(request,
                  'webapp/main_page.html')


def general_form_data(form_data):
    return {
        'PRD_identification_number': form_data.cleaned_data['PRD_identification_number'],
        'PRD_function': form_data.cleaned_data['PRD_function'],
        'Installation_of_PRD': form_data.cleaned_data['Installation_of_PRD'],
        'RBI_assessment_date': form_data.cleaned_data['RBI_assessment_date'],
        'Type_of_PRD': form_data.cleaned_data['Type_of_PRD'],
        'PRD_Containing_Soft_Seats': form_data.cleaned_data['PRD_Containing_Soft_Seats'],
        'PRD_set': form_data.cleaned_data['PRD_set'],
        'Service_severity': form_data.cleaned_data['Service_severity'],
        'PRD_Discharge_Location': form_data.cleaned_data['PRD_Discharge_Location'],
        'Environment_Factor_Modifier': form_data.cleaned_data['Environment_Factor_Modifier'],
        'Rupture_disk_is_installed_upstream_of_PRD': form_data.cleaned_data['Rupture_disk_is_installed_upstream_of_PRD']
    }


def form_inspection_data(form_data):
    return {
        'Fixed_Equipment_Protected_by_PRD': form_data.cleaned_data['Fixed_Equipment_Protected_by_PRD'],
        'Protected_Equipment_Demage_Status': form_data.cleaned_data['Protected_Equipment_Demage_Status'],
        'Maximum_Allow_able_Working_Pressure_of_Protected_Equipment': form_data.cleaned_data['Maximum_Allow_able_Working_Pressure_of_Protected_Equipment'],
        'Operating_Pressure_of_the_Protected_Equipment': form_data.cleaned_data['Operating_Pressure_of_the_Protected_Equipment'],
        'management_system_factor': form_data.cleaned_data['management_system_factor']
    }


def failure_to_open_data(form_data):
    return {
        'Multiple_PRDs_protecting_fixed_equipment': form_data.cleaned_data['Multiple_PRDs_protecting_fixed_equipment'],
        'Orifice_area_of_the_PRD': form_data.cleaned_data['Orifice_area_of_the_PRD'],
        'Total_installed_orifice_area_of_a_multiple_PDRs_installation': form_data.cleaned_data['Total_installed_orifice_area_of_a_multiple_PDRs_installation']
    }


def failure_of_leakage_data(form_data):
    return {
        'Rated_Capacity_of_PRD': form_data.cleaned_data['Rated_Capacity_of_PRD'],
        'PRD_Inlet_Size': form_data.cleaned_data['PRD_Inlet_Size'],
        'Cost_of_the_fluid': form_data.cleaned_data['Cost_of_the_fluid'],
        'Environmental_clean_up_costs_due_to_a_PRD_leakage': form_data.cleaned_data['Environmental_clean_up_costs_due_to_a_PRD_leakage'],
        'PRD_leakage_can_be_tolered': form_data.cleaned_data['PRD_leakage_can_be_tolered'],
        'Cost_of_shutdown_to_repair_PRD': form_data.cleaned_data['Cost_of_shutdown_to_repair_PRD'],
        'Daily_production_margin_on_the_unit': form_data.cleaned_data['Daily_production_margin_on_the_unit'],
        'Days_required_to_shutdown_a_unit_to_repair_a_leakage': form_data.cleaned_data['Days_required_to_shutdown_a_unit_to_repair_a_leakage']
    }


def inspection_history_data(form_data):
    return {
        'RBI_inspection_test_date': form_data.cleaned_data['RBI_inspection_test_date'],
        'PRD_pop_test_results': form_data.cleaned_data['PRD_pop_test_results'],
        'PRD_Leakage_results': form_data.cleaned_data['PRD_Leakage_results'],
        'PRD_Inspection_Effectiveness': form_data.cleaned_data['PRD_Inspection_Effectiveness'],
        'PRD_Overhauled_during_the_inspection': form_data.cleaned_data['PRD_Overhauled_during_the_inspection'],
        'PRD_replace_with_new_PRD_in_lieu_of_overhaul': form_data.cleaned_data['PRD_replace_with_new_PRD_in_lieu_of_overhaul']
    }



def applicable_overpressure_data(form_data):
    return {
        'Over_pressure_demand_case': form_data.cleaned_data['Over_pressure_demand_case'],
        'Overpressure_associated_with_the_overpressure': form_data.cleaned_data['Overpressure_associated_with_the_overpressure'],
        'PRD_COF_to_open_associated_with_jth_overpressure': form_data.cleaned_data['PRD_COF_to_open_associated_with_jth_overpressure']
    }


def format_word(word):
    word = word.split('_')
    formatted_word = ""
    formatted_word += word[0].capitalize()
    for w in word[1:]:
        formatted_word += (" " + w)
    return formatted_word


def save_to_scv(objs):
    fieldnames = ['id', 'RBI_inspection_test_date', 'PRD_pop_test_results',
                  'PRD_Leakage_results', 'PRD_Inspection_Effectiveness',
                  'PRD_Overhauled_during_the_inspection',
                  'PRD_replace_with_new_PRD_in_lieu_of_overhaul']

    with open('inspection_history.csv', 'w+', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(fieldnames)

        for obj in objs:
            date_ = obj.RBI_inspection_test_date
            val = ""
            if date_ is not None:
                val = str(date_)
            else:
                val = ""
            writer.writerow([
                obj.pk,
                str(val),
                format_word(obj.PRD_pop_test_results),
                format_word(obj.PRD_Leakage_results),
                format_word(obj.PRD_Inspection_Effectiveness),
                format_word(obj.PRD_Overhauled_during_the_inspection),
                format_word(obj.PRD_replace_with_new_PRD_in_lieu_of_overhaul)
            ])



def check_time(time):
    if time is not None:
        t = datetime.date(time)
    else:
        t = ""
    return t


def fetch_history_case_one():
    objects_history_data = []
    inspec_history_objs = Prd_InspectionHistory.objects.all()
    save_to_scv(inspec_history_objs)
    index = 1
    for obj in inspec_history_objs:
        values = []
        values.append(index)
        values.append(obj.RBI_inspection_test_date)
        values.append(format_word(obj.PRD_pop_test_results))
        values.append(format_word(obj.PRD_Leakage_results))
        values.append(format_word(obj.PRD_Inspection_Effectiveness))
        values.append(format_word(obj.PRD_Overhauled_during_the_inspection))
        values.append(format_word(obj.PRD_replace_with_new_PRD_in_lieu_of_overhaul))
        values.append(obj.pk)
        objects_history_data.append(values)
        index += 1

    return objects_history_data



def fetch_history_case_two():
    objects_history_data = []
    inspec_history_objs = Prd_InspectionHistory.objects.all()
    save_to_scv(inspec_history_objs)
    first_installation = GeneralInformation.objects.first()
    first_installation = first_installation.Installation_of_PRD
    index = 1
    for obj in inspec_history_objs:
        values = []
        tdur = obj.RBI_inspection_test_date - first_installation
        tdur = tdur.days / 365
        values.append(index)
        values.append(obj.RBI_inspection_test_date)
        values.append(format_word(obj.PRD_pop_test_results))
        values.append(format_word(obj.PRD_Inspection_Effectiveness))
        values.append(format_word(obj.PRD_Overhauled_during_the_inspection))
        values.append(format_word(obj.PRD_replace_with_new_PRD_in_lieu_of_overhaul))
        values.append(tdur)
        values.append(obj.pk)
        objects_history_data.append(values)
        index += 1

    return objects_history_data




def fetch_history_case_two_leakage():
    objects_history_data = []
    inspec_history_objs = Prd_InspectionHistory.objects.all()
    save_to_scv(inspec_history_objs)
    first_installation = GeneralInformation.objects.first()
    first_installation = first_installation.Installation_of_PRD
    index = 1
    for obj in inspec_history_objs:
        values = []
        tdur = obj.RBI_inspection_test_date - first_installation
        tdur = tdur.days / 365
        values.append(index)
        values.append(check_time(obj.RBI_inspection_test_date))
        values.append(format_word(obj.PRD_Leakage_results))
        values.append(format_word(obj.PRD_Inspection_Effectiveness))
        values.append(format_word(obj.PRD_Overhauled_during_the_inspection))
        values.append(format_word(obj.PRD_replace_with_new_PRD_in_lieu_of_overhaul))
        values.append(tdur)
        values.append(obj.pk)
        objects_history_data.append(values)
        index += 1

    return objects_history_data



def fetch_history_case_four():
    objects_history_data = []
    inspec_history_objs = Prd_InspectionHistory.objects.all()
    save_to_scv(inspec_history_objs)
    first_installation = GeneralInformation.objects.first() #first()
    first_installation = first_installation.Installation_of_PRD
    index = 1
    for obj in inspec_history_objs:
        # initial_installation = first_installation
        values = []
        values.append(index)
        values.append(obj.RBI_inspection_test_date)
        values.append(format_word(obj.PRD_pop_test_results))
        values.append(format_word(obj.PRD_Inspection_Effectiveness))
        values.append(format_word(obj.PRD_Overhauled_during_the_inspection))
        values.append(format_word(obj.PRD_replace_with_new_PRD_in_lieu_of_overhaul))
        if format_word(obj.PRD_Overhauled_during_the_inspection) == 'Yes':
            tdur = obj.RBI_inspection_test_date - first_installation
            print(f'{obj.RBI_inspection_test_date} - {first_installation} = {(obj.RBI_inspection_test_date - first_installation).days / 365}')
            first_installation = obj.RBI_inspection_test_date
            tdur = tdur.days / 365
            values.append(tdur)
        else:
            tdur = obj.RBI_inspection_test_date - first_installation
            print(f'{obj.RBI_inspection_test_date} - {first_installation} = {(obj.RBI_inspection_test_date - first_installation).days / 365}')
            tdur = tdur.days / 365
            values.append(tdur)

        values.append(obj.pk)
        objects_history_data.append(values)
        index += 1

    return objects_history_data




def fetch_history_case_five():
    objects_history_data = []
    inspec_history_objs = Prd_InspectionHistory.objects.all()
    save_to_scv(inspec_history_objs)
    first_installation = GeneralInformation.objects.first() #first()
    first_installation = first_installation.Installation_of_PRD
    index = 1
    for obj in inspec_history_objs:
        # print(first_installation)
        values = []
        values.append(index)
        values.append(obj.RBI_inspection_test_date)
        values.append(format_word(obj.PRD_pop_test_results))
        values.append(format_word(obj.PRD_Inspection_Effectiveness))
        values.append(format_word(obj.PRD_Overhauled_during_the_inspection))
        values.append(format_word(obj.PRD_replace_with_new_PRD_in_lieu_of_overhaul))
        if format_word(obj.PRD_Overhauled_during_the_inspection) == 'Yes':
            tdur = obj.RBI_inspection_test_date - first_installation
            first_installation = obj.RBI_inspection_test_date
            tdur = tdur.days / 365
            values.append(tdur)
        elif format_word(obj.PRD_replace_with_new_PRD_in_lieu_of_overhaul) == 'Yes':
            tdur = obj.RBI_inspection_test_date - first_installation
            first_installation = obj.RBI_inspection_test_date
            tdur = tdur.days / 365
            values.append(tdur)
        else:
            tdur = obj.RBI_inspection_test_date - first_installation
            tdur = tdur.days / 365
            values.append(tdur)
        # print(tdur)

        values.append(obj.pk)
        objects_history_data.append(values)
        index += 1

    return objects_history_data






def create_data_case_two():
    data = fetch_history_case_two()
    writer = csv.writer(['index', 'RBI_inspection_test_date', 'PRD_pop_test_results',
                         'PRD_Inspection_Effectiveness', 'PRD_Overhauled_during_the_inspection',
                         'PRD_replace_with_new_PRD_in_lieu_of_overhaul', 'tdur'])
    for row in data:
        for val in row[:-1]:
            writer.writerow([val[0], val[1], val[2], val[3], val[4], val[5], val[6], val[7]])


def save_case_two(row):
    with open('case_two.csv', 'a', newline='') as csv_file:
        writer = csv.writer(csv_file)

        writer.writerow([val for val in row])


def save_case(row, filename):
    with open(filename, 'a', newline='') as csv_file:
        writer = csv.writer(csv_file)

        writer.writerow([val for val in row])



def save_case_four(row):
    with open('case_four.csv', 'a', newline='') as csv_file:
        writer = csv.writer(csv_file)

        writer.writerow([val for val in row])


def save_case_five(row):
    with open('case_five.csv', 'a', newline='') as csv_file:
        writer = csv.writer(csv_file)

        writer.writerow([val for val in row])



def save_case_six(row):
    with open('case_six.csv', 'a', newline='') as csv_file:
        writer = csv.writer(csv_file)

        writer.writerow([val for val in row])


def save_overpressure_demand_case(row):
    with open('overpressure_demand.csv', mode='a', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow([val for val in row])



def fetch_applicable_overpressure():
    applicable_overpressure_data = []
    applicable_overpr_objs = ApplicableOverpressureDemandCase.objects.all()
    index=1
    for obj in applicable_overpr_objs:
        values = []
        values.append(index)
        values.append(obj.Over_pressure_demand_case)
        values.append(obj.Overpressure_associated_with_the_overpressure)
        values.append(obj.PRD_COF_to_open_associated_with_jth_overpressure)
        applicable_overpressure_data.append(values)
        values.append(0)
        values.append(0)
        values.append(0)
        values.append(0)
        values.append(0)
        values.append(obj.pk)
        index += 1
    return applicable_overpressure_data


def fetch_obj_ids(data):
    ids = []
    for val in data:
        ids.append(val[0])
    return ids



def save_inspec_histo_data(data):
    with open('history_data.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([val for val in data])


@login_required(login_url='/prd/login')
def delete_inspe_history_obj(request, pk=None):
    object = get_object_or_404(Prd_InspectionHistory, pk=pk)
    object.delete()
    return redirect('/prd/create_prd/')




@login_required(login_url='/prd/login')
def delete_applic_overpr_obj(request, pk=None):
    object = get_object_or_404(ApplicableOverpressureDemandCase, pk=pk)
    object.delete()
    return redirect('/prd/create_prd/')



def create_dict_insp_data(data):
    values = []
    for val in data:
        inspe_date = val[1]
        pop_test_resul = val[2]
        prd_Leakage_results = val[3]
        inspe_eff = val[4]
        prd_overhauled = val[5]
        prd_replaced = val[6]
        elem = {
            'Inspection_test_data': inspe_date,
            'Pop_test_result': pop_test_resul,
            'PRD_Leakage_results': prd_Leakage_results,
            'Inspection_Effectiveness': inspe_eff,
            'Prd_overhauled':  prd_overhauled,
            'Prd_replaced': prd_replaced
        }
        values.append(elem)

    return values




def create_dict_insp_leakage_data(data):
    values = []
    for val in data:
        inspe_date = val[1]
        pop_test_resul = val[2]
        prd_Leakage_results = val[3]
        inspe_eff = val[4]
        prd_overhauled = val[5]
        prd_replaced = val[6]
        elem = {
            'Inspection_test_data': inspe_date,
            'Pop_test_result': pop_test_resul,
            'PRD_pop_test_results': prd_Leakage_results,
            'Inspection_Effectiveness': inspe_eff,
            'Prd_overhauled':  prd_overhauled,
            'Prd_replaced': prd_replaced
        }
        values.append(elem)

    return values




def determine_case_one_leakage_result(data):
    values = create_dict_insp_data(data)

    check_case = False
    for row in values:
        print(row)
        if ((row['Inspection_test_data'] == '' and
             row['PRD_Leakage_results'] == 'None' and
             row['Inspection_Effectiveness'] == 'None') and
             (row['Prd_overhauled'] == 'None' and
             row['Prd_replaced'] == 'None')):

            check_case = True

    return check_case




def determine_case_one():
    objs = Prd_InspectionHistory.objects.all()
    return objs.count() == 1



def determine_case_two(data):
    values = create_dict_insp_data(data)

    check_case = False
    if len(values) > 1:
        for row in values:
            if (row['Inspection_test_data'] != '' and
                 row['Pop_test_result'] != 'None' and
                 row['Inspection_Effectiveness'] != 'None' and
                 row['Prd_overhauled'] == 'No' and
                 row['Prd_replaced'] == 'No'):

                check_case = True

            if (row['Prd_overhauled'] == 'Yes' or
                row['Prd_replaced'] == 'Yes'):
                return False

    return check_case


def determine_case_three(data):
    values = create_dict_insp_data(data)

    check_case = 0
    if len(values) == 1:
        for row in values:
            if ((row['Inspection_test_data'] != '' and
                 row['Pop_test_result'] == 'None' and
                 row['Inspection_Effectiveness'] == 'None') and
                 (row['Prd_overhauled'] == 'Yes' and
                 row['Prd_replaced'] == 'No')):

                check_case += 1

    return check_case == 1


def determine_case_four(data):
    values = create_dict_insp_data(data)

    count = 0
    if len(values) > 1:
        for row in values:
            if (type(row['Inspection_test_data']) == dt.date and
                row['Pop_test_result'] == 'None' and
                row['Inspection_Effectiveness'] == 'None' and
                row['Prd_overhauled'] == 'Yes' and
                row['Prd_replaced'] == 'No'):
                count += 1

            if row['Prd_replaced'] == 'Yes':
                return False

    return count == 1 #and check_case



def determine_case_five(data):
    values = create_dict_insp_data(data)

    count = 0
    check_case = False
    for row in values:
        if (type(row['Inspection_test_data']) == dt.date and
            row['Pop_test_result'] == 'None' and
            row['Inspection_Effectiveness'] == 'None'):

            if (row['Prd_overhauled'] == 'Yes' and
                row['Prd_replaced'] == 'No'):
                count += 1

            if (row['Prd_overhauled'] == 'No' and
                row['Prd_replaced'] == 'Yes'):
                check_case = True

    return count >= 1 and check_case


def determine_case_six(data):
    values = create_dict_insp_data(data)

    count = 0
    if len(values) > 1:
        for row in values:
            if (type(row['Inspection_test_data']) != '' and
                row['Pop_test_result'] == 'None' and
                row['Inspection_Effectiveness'] == 'None' and
                row['Prd_overhauled'] == 'Yes' and
                row['Prd_replaced'] == 'No'):
                count += 1

            if row['Prd_replaced'] == 'Yes':
                return False

    return count > 1




def determine_case_two_leakage(data):
    values = create_dict_insp_data(data)

    check_case = False
    if len(values) > 1:
        for row in values:
            if (row['Inspection_test_data'] != '' and
                 row['PRD_Leakage_results'] != 'None' and
                 row['Inspection_Effectiveness'] != 'None' and
                 row['Prd_overhauled'] == 'No' and
                 row['Prd_replaced'] == 'No'):

                check_case = True

            if (row['Prd_overhauled'] == 'Yes' or
                row['Prd_replaced'] == 'Yes'):
                return False

    return check_case



def determine_case_three_leakage(data):
    values = create_dict_insp_data(data)

    check_case = 0
    if len(values) == 1:
        for row in values:
            if ((row['Inspection_test_data'] != '' and
                 row['PRD_Leakage_results'] == 'None' and
                 row['Inspection_Effectiveness'] == 'None') and
                 (row['Prd_overhauled'] == 'Yes' and
                 row['Prd_replaced'] == 'No')):

                check_case += 1

    return check_case == 1




def determine_case_four_leakage(data):
    values = create_dict_insp_data(data)
    count = 0
    if len(values) > 1:
        for row in values:
            if (type(row['Inspection_test_data']) == dt.date and
                row['PRD_Leakage_results'] != 'None' and
                row['Inspection_Effectiveness'] != 'None' and
                row['Prd_overhauled'] == 'Yes' and
                row['Prd_replaced'] == 'No'):
                count += 1

            if row['Prd_replaced'] == 'Yes':
                return False
    return count == 1



def determine_case_five_leakage(data):
    values = create_dict_insp_data(data)
    count = 0
    check_case = False
    for row in values:
        if (type(row['Inspection_test_data']) == dt.date and
            row['PRD_Leakage_results'] == 'None' and
            row['Inspection_Effectiveness'] == 'None'):

            if (row['Prd_overhauled'] == 'Yes' and
                row['Prd_replaced'] == 'No'):
                count += 1

            if (row['Prd_overhauled'] == 'No' and
                row['Prd_replaced'] == 'Yes'):
                check_case = True

    return check_case >= 1 and check_case



def determine_case_six_leakage(data):
    values = create_dict_insp_data(data)

    count = 0
    if len(values) > 1:
        for row in values:
            if (type(row['Inspection_test_data']) != '' and
                row['PRD_Leakage_results'] == 'None' and
                row['Inspection_Effectiveness'] == 'None' and
                row['Prd_overhauled'] == 'Yes' and
                row['Prd_replaced'] == 'No'):
                count += 1

            if row['Prd_replaced'] == 'Yes':
                return False

    return count > 1



def format_decimal(decimal):
    return float('{:.9f}'.format(decimal))


def empty_general_info():
    objects = GeneralInformation.objects.all()
    for obj in objects:
        obj.delete()

@login_required(login_url='/prd/login/')
def create_prd(request):
    empty_general_info()
    objects_history_data = fetch_history_case_one()
    fetch_obj_ids(objects_history_data)
    applicable_overpress_data = fetch_applicable_overpressure()
    form_general = GeneralInformationForm(request.POST)
    form_inspection = PRD_InspectionForm(request.POST)
    failure_to_open_form = ConsequencesOfFailureInputDataForm(request.POST)
    failure_of_leakage_form = Consequences0fFailureOfLeakageForm(request.POST)
    inspection_history = Prd_InspectionHistoryForm(request.POST)
    applicable_overpressure = ApplicableOverpressureDemandCaseForm(request.POST)
    values = []
    t, p_fod, p_pol, p_prd_l = 0, 0, 0, 0



    if request.method == 'POST':
        data = dict()
        if form_general.is_valid():
            form_1 = general_form_data(form_general)
            form_general.save(commit=True)
            data.update(form_1)

        if form_inspection.is_valid():
            form_2 = form_inspection_data(form_inspection)
            form_inspection.save(commit=True)
            data.update(form_2)

        if failure_to_open_form.is_valid():
            form_3 = failure_to_open_data(failure_to_open_form)
            failure_to_open_form.save(commit=True)
            data.update(form_3)

        if failure_of_leakage_form.is_valid():
            form_4 = failure_of_leakage_data(failure_of_leakage_form)
            failure_to_open_form.save(commit=True)
            data.update(form_4)

        if inspection_history.is_valid():
            form_5 = inspection_history_data(inspection_history)
            data.update(form_5)
            inspection_history.save(commit=True)
            objects_history_data = fetch_history_case_one()
            date_ = data['RBI_inspection_test_date']
            if date_ is not None:
                values.append(date_)
            else:
                values.append("")
            pop_result = data['PRD_pop_test_results']
            if pop_result is not None:
                values.append(pop_result)
            else:
                values.append("")
            # values.append(data['PRD_Leakage_results'])
            values.append(format_word(data['PRD_Inspection_Effectiveness']))
            values.append(data['PRD_Overhauled_during_the_inspection'])
            values.append(data['PRD_replace_with_new_PRD_in_lieu_of_overhaul'])


        if applicable_overpressure.is_valid():
            form_6 = applicable_overpressure_data(applicable_overpressure)
            data.update(form_6)
            applicable_overpressure.save(commit=True)
            applicable_overpress_data = fetch_applicable_overpressure()


            print('\n\n********** PRD PROBABILITY OF FAILURE **********')
            print('-' * 100)

            b = 1.8
            print(f'b_pod = {b}')
            n_def_value = n_def['fuild_severity'][data['Service_severity']][data['Type_of_PRD']]
            print(f'n_def_pod = {n_def_value}')

            fc_value = Fc_POD(data['Type_of_PRD'], data['PRD_Discharge_Location'])
            print(f'fc_pod = {fc_value}')

            fc_env_val = F_env_POD[data['Environment_Factor_Modifier']]
            print(f'fc_env_pod = {fc_env_val}')

            n_mod_value = fc_value * fc_env_val * n_def_value
            print(f'n_mod_pod = {n_mod_value}')


            if determine_case_one():
               # first_installation = GeneralInformation.objects.first() #first()
               RBI_assessment_date = data['RBI_assessment_date']
               instalation_date = data['Installation_of_PRD']
               years = (RBI_assessment_date - instalation_date).days / 365
               years = float(f'{years:.9f}')
               t = years
               print(f'\n\nt = {years}')
               p_fod = 1 - math.e**(-(t/n_mod_value)**1.8)
               p_fod = float(f'{p_fod:.9f}')
               print(f'p_fod = {p_fod}\n\n')
               with open('case_one.csv', mode='a', newline='') as file:
                   writer = csv.writer(file)
                   writer.writerow([t, p_fod])




            if determine_case_three(objects_history_data):
                values = fetch_history_case_two()
                RBI_assessment_date = data.get('RBI_assessment_date').date()
                t = 0
                insp = 0
                for row in values[0:2]:
                    insp = row[1]
                    t = (RBI_assessment_date - row[1]).days / 365
                p_fod = 1 - math.e**(-((t/n_mod_value)**1.8))
                with open('case_three.csv', mode='a', newline='') as file:
                   writer = csv.writer(file)
                   writer.writerow([t, p_fod])
                print('\n\n')
                print(f'RBI date = {RBI_assessment_date}')
                print(f'Inspection test = {insp}')
                print(f't = {t}')
                print(f'p_fod = {p_fod}')
                print('\n\n')




            if determine_case_two(objects_history_data):
                values = fetch_history_case_two()
                first_installation = GeneralInformation.objects.first() #first()
                first_installation = first_installation.Installation_of_PRD
                inspection_date = data['RBI_assessment_date']
                years = (inspection_date - first_installation).days / 365
                years = float(f'{years:.9f}')
                p_prd_f_prior = 0
                n_mod = n_mod_value
                t = 0
                eta_updated = 0
                for row in values:
                    print('\n')
                    if row[3] == 'None':
                        pass
                    else:
                        if values[0][0] == 1:
                            try:
                                t = row[6]
                                p_prd_f_prior = 1 - math.e**(-((t/n_mod)**b))
                            except ZeroDivisionError:
                                p_prd_f_cond = 0
                        else:
                            t = row[6]
                            p_prd_f_prior = 1 - math.e**(-((t/n_mod)**b))
                        p_prd_f_prior = float('{:.9f}'.format(p_prd_f_prior))
                        print(f'p_prd_f_prior = {p_prd_f_prior}')
                        p_prd_p_prior = 1 - p_prd_f_prior
                        print(f'p_prd_p_prior = {p_prd_p_prior}')
                        row.append(p_prd_f_prior)
                        row.append(p_prd_p_prior)

                        p_prd_f_cond = 0
                        first, second = row[3].split(' ')
                        first = first.lower()
                        result = '_'.join([first, second])
                        cf_pass = CF['Inspection_Result']['pass'][result]
                        cf_fail = CF['Inspection_Result']['fail'][result]
                        if row[2] == 'Pass':
                            p_prd_f_cond = (1 - cf_pass) * p_prd_p_prior
                        elif row[2] == 'Fail':
                            p_prd_f_cond = cf_fail * p_prd_f_prior + (1 - cf_pass) * p_prd_p_prior

                        # if isinstance(p_prd_f_cond, complex):
                            # p_prd_f_cond = p_prd_f_cond.real
                        p_prd_f_cond = float('{:.9f}'.format(p_prd_f_cond))
                        print(f'p_prd_f_cond = {p_prd_f_cond}')
                        row.append(p_prd_f_cond)

                        if ((row[3] == 'Highly effective' and row[2] == 'Pass') or
                            (row[3] == 'Usually effective' and row[2] == 'Pass') or
                            (row[3] == 'Faily effective' and row[2] == 'Pass')):
                            p_prd_f_wgt = p_prd_f_prior - 0.2 * p_prd_f_prior*(row[6]/n_mod) + 0.2*(p_prd_f_cond*(row[6]/n_mod))
                        elif ((row[3] == 'Highly effective' and row[2] == 'Fail') or
                              (row[3] == 'Usually effective' and row[2] == 'Fail')):
                            p_prd_f_wgt = p_prd_f_cond
                        elif (row[3] == 'Faily effective' and row[2] == 'Fail'):
                            p_prd_f_wgt = 0.5 * p_prd_f_prior + 0.5 * p_prd_f_cond
                        p_prd_f_wgt = float('{:.9f}'.format(p_prd_f_wgt))
                        print(f'p_prd_f_wgt = {p_prd_f_wgt}')
                        row.append(p_prd_f_wgt)

                        val = 1 - p_prd_f_wgt
                        e = float(f'{math.e:.9f}')
                        ln = -math.log(val, e)
                        b_val = (1/1.8)
                        eta_updated = row[6] / (ln**b_val)
                        eta_updated = float('{:.9f}'.format(eta_updated))
                        print(f'eta_updated = {eta_updated}')
                        row.append(eta_updated)
                        save_case_two(row)
                        n_mod = eta_updated
                        print(row[6])
                        print('\n')
                p_fod = 1-math.e**(-((years/n_mod)**1.8))
                p_fod = float(f'{p_fod:.9f}')
                print(f't = {years}')
                print(f'p_fod = {p_fod}')


                # F_set = F_set_formula(data['Type_of_PRD'], data['PRD_set'], data['Operating_Pressure_of_the_Protected_Equipment'])
                # print(f'F_set = {F_set}')


                # if data['Rupture_disk_is_installed_upstream_of_PRD'] == 'no':
                #     p_prd_l = p_fod * F_set
                # else:
                #     p_prd_l = 0
                # print(f'p_prd_l = {p_prd_l}')
                # print('->' * 50)





            if determine_case_four(objects_history_data):
                values = fetch_history_case_four()
                first_installation = GeneralInformation.objects.first() #first()
                first_installation = first_installation.Installation_of_PRD
                inspection_date = data['RBI_assessment_date']
                years = (inspection_date - first_installation).days / 365
                p_prd_f_prior = 0
                n_mod = n_mod_value
                t = 0
                eta_updated = 0
                # n_updated = 0
                E = format_decimal(math.e)
                for row in values:
                    print(row)
                    print('\n')
                    tdur = row[6]
                    if row[3] == 'None':
                        p_prd_f_prior, p_prd_p_prior = '', ''
                        p_prd_f_cond, p_prd_f_wgt = '', ''
                        eta_updated = 17.6
                        n_updated = eta_updated
                        row.append(p_prd_f_prior)
                        row.append(p_prd_p_prior)
                        row.append(p_prd_f_cond)
                        row.append(p_prd_f_wgt)
                        row.append(eta_updated)
                    else:
                        if row[0] == 1:
                            try:
                                p_prd_f_prior = 1 - math.e**(-((tdur/n_mod)**1.8))
                            except ZeroDivisionError:
                                p_prd_f_prior = 0
                        else:
                            t = row[6]
                            p_prd_f_prior = 1 - math.e**(-((tdur/n_mod)**1.8))
                        p_prd_f_prior = format_decimal(p_prd_f_prior)
                        print(f'p_prd_f_prior = {p_prd_f_prior}')
                        p_prd_p_prior = 1 - p_prd_f_prior
                        p_prd_p_prior = format_decimal(p_prd_p_prior)
                        print(f'p_prd_p_prior = {p_prd_p_prior}')
                        row.append(p_prd_f_prior)
                        row.append(p_prd_p_prior)

                        p_prd_f_cond = 0
                        first, second = row[3].split(' ')
                        first = first.lower()
                        result = '_'.join([first, second])
                        cf_pass = CF['Inspection_Result']['leak'][result]
                        cf_fail = CF['Inspection_Result']['no_leak'][result]
                        if row[2] == 'Pass':
                            p_prd_f_cond = (1 - 0.7) * p_prd_p_prior
                        elif row[2] == 'Fail':
                            if row[2] == 'Fail' and row[3] == 'Highly effective':
                                p_prd_f_cond = 0.95 * p_prd_f_prior + (1 - 0.9) * p_prd_p_prior
                            else:
                                p_prd_f_cond = 0.95 * p_prd_f_prior + (1 - 0.7) * p_prd_p_prior

                        # if isinstance(p_prd_f_cond, complex):
                            # p_prd_f_cond = p_prd_f_cond.real
                        p_prd_f_cond = float('{:.9f}'.format(p_prd_f_cond))
                        print(f'p_prd_f_cond = {p_prd_f_cond}')
                        row.append(p_prd_f_cond)

                        if row[0] == 1:
                            if ((row[3] == 'Highly effective' and row[2] == 'Pass') or
                                (row[3] == 'Usually effective' and row[2] == 'Pass') or
                                (row[3] == 'Faily effective' and row[2] == 'Pass')):
                                p_prd_f_wgt = p_prd_f_prior - (0.2 * p_prd_f_prior*(tdur/n_mod)) + 0.2*(p_prd_f_cond*(tdur/n_mod))
                            elif ((row[3] == 'Highly effective' and row[2] == 'Fail') or
                                  (row[3] == 'Usually effective' and row[2] == 'Fail')):
                                p_prd_f_wgt = p_prd_f_cond
                            elif (row[3] == 'Faily effective' and row[2] == 'Fail'):
                                p_prd_f_wgt = 0.5 * p_prd_f_prior + 0.5 * p_prd_f_cond
                        else:
                            if ((row[3] == 'Highly effective' and row[2] == 'Pass') or
                                (row[3] == 'Usually effective' and row[2] == 'Pass') or
                                (row[3] == 'Faily effective' and row[2] == 'Pass')):
                                p_prd_f_wgt = p_prd_f_prior - 0.2 * p_prd_f_prior*(tdur/n_mod) + 0.2*(p_prd_f_cond*(tdur/n_mod))
                            elif ((row[3] == 'Highly effective' and row[2] == 'Fail') or
                                  (row[3] == 'Usually effective' and row[2] == 'Fail')):
                                p_prd_f_wgt = p_prd_f_cond
                            elif (row[3] == 'Faily effective' and row[2] == 'Fail'):
                                p_prd_f_wgt = 0.5 * p_prd_f_prior + 0.5 * p_prd_f_cond

                        # if isinstance(p_prd_f_wgt, complex):
                            # p_prd_f_wgt = p_prd_f_wgt.real
                        p_prd_f_wgt = format_decimal(p_prd_f_wgt)
                        print(f'p_prd_f_wgt = {p_prd_f_wgt}')
                        row.append(p_prd_f_wgt)

                        val = 1 - p_prd_f_wgt
                        ln = -math.log(val, E)
                        b_1 = (1/1.8)
                        try:
                            eta_updated = row[6] / (ln**b_1)
                        except ZeroDivisionError:
                            eta_updated = 0
                        # if isinstance(eta_updated, complex):
                            # eta_updated = n_updated.real
                        eta_updated = format_decimal(eta_updated)
                        print(f'eta_updated = {eta_updated}')
                        row.append(eta_updated)
                        n_mod= eta_updated
                    if row[4] == 'Yes':
                        n_mod = n_mod_value
                        years = (data['RBI_assessment_date'].date() - row[1]).days / 365
                    save_case_four(row)
                    print('\n')


                p_fod = 1-math.e**(-((years/n_mod)**1.8))
                print(f't = {years}')
                print(f'p_fod = {p_fod}')
                print('\n\n')


                F_set = F_set_formula(data['Type_of_PRD'], data['PRD_set'], data['Operating_Pressure_of_the_Protected_Equipment'])
                print(f'F_set = {F_set}')


                if data['Rupture_disk_is_installed_upstream_of_PRD'] == 'no':
                    p_prd_l = p_fod * F_set
                else:
                    p_prd_l = 0
                print(f'p_prd_l = {p_prd_l}')



            if determine_case_five(objects_history_data):
                values = fetch_history_case_five()
                first_installation = GeneralInformation.objects.first() #first()
                first_installation = first_installation.Installation_of_PRD
                inspection_date = data['RBI_assessment_date']
                years = (inspection_date - first_installation).days / 365
                p_prd_f_prior = 0
                n_mod = n_mod_value
                t = 0
                eta_updated = 0
                inspc_date = 0
                E = format_decimal(math.e)
                for row in values:
                    print('\n')
                    print(f'n_mod = {n_mod}')
                    tdur = format_decimal(row[6])
                    if row[4] == 'Yes' or row[5] == 'Yes':
                        n_mod = n_mod_value
                    else:
                        if row[0] == 1:
                            try:
                                p_prd_f_prior = 1 - E**(-((tdur/n_mod)**1.8))
                                print(f'p_prd_f_prior = 1 - {E}**(-(({tdur}/{n_mod})**{1.8}))')
                            except ZeroDivisionError:
                                p_prd_f_prior = 0
                        else:
                            t = row[6]
                            p_prd_f_prior = 1 - E**(-((tdur/n_mod)**1.8))
                            print(f'p_prd_f_prior = 1 - {E}**(-(({tdur}/{n_mod})**{1.8}))')
                        p_prd_f_prior = format_decimal(p_prd_f_prior)
                        print(f'p_prd_f_prior = {p_prd_f_prior}')
                        p_prd_p_prior = 1 - p_prd_f_prior
                        p_prd_p_prior = format_decimal(p_prd_p_prior)
                        print(f'p_prd_p_prior = {p_prd_p_prior}')
                        row.append(p_prd_f_prior)
                        row.append(p_prd_p_prior)

                        p_prd_f_cond = 0
                        first, second = row[3].split(' ')
                        first = first.lower()
                        result = '_'.join([first, second])
                        cf_pass = CF['Inspection_Result']['pass'][result]
                        cf_fail = CF['Inspection_Result']['fail'][result]
                        if row[2] == 'Pass':
                            p_prd_f_cond = (1 - cf_pass) * p_prd_p_prior
                        elif row[2] == 'Fail':
                            p_prd_f_cond = cf_fail * p_prd_f_prior + (1 - cf_pass) * p_prd_p_prior

                        # if isinstance(p_prd_f_cond, complex):
                            # p_prd_f_cond = p_prd_f_cond.real
                        p_prd_f_cond = float('{:.9f}'.format(p_prd_f_cond))
                        print(f'p_prd_f_cond = {p_prd_f_cond}')
                        row.append(p_prd_f_cond)


                        p_prd_f_wgt = ''
                        if row[0] == 1:
                            if ((row[3] == 'Highly effective' and row[2] == 'Pass') or
                                (row[3] == 'Usually effective' and row[2] == 'Pass') or
                                (row[3] == 'Faily effective' and row[2] == 'Pass')):
                                print('First')
                                print(f'p_prd_f_wgt = {p_prd_f_prior} - (0.2 * {p_prd_f_prior}*({tdur}/{n_mod})) + 0.2*({p_prd_f_cond}*({tdur}/{n_mod}))')
                                p_prd_f_wgt = p_prd_f_prior - (0.2 * p_prd_f_prior*(tdur/n_mod)) + 0.2*(p_prd_f_cond*(tdur/n_mod))
                            elif ((row[3] == 'Highly effective' and row[2] == 'Fail') or
                                  (row[3] == 'Usually effective' and row[2] == 'Fail')):
                                print('Second')
                                print(f'p_prd_f_wgt = {p_prd_f_cond}')
                                p_prd_f_wgt = p_prd_f_cond
                            elif (row[3] == 'Faily effective' and row[2] == 'Fail'):
                                print('Third')
                                print(f'p_prd_f_wgt = 0.5 * {p_prd_f_prior} + 0.5 * {p_prd_f_cond}')
                                p_prd_f_wgt = 0.5 * p_prd_f_prior + 0.5 * p_prd_f_cond
                        else:
                            if ((row[3] == 'Highly effective' and row[2] == 'Pass') or
                                (row[3] == 'Usually effective' and row[2] == 'Pass') or
                                (row[3] == 'Faily effective' and row[2] == 'Pass') or
                                (row[3] == 'Highly ineffective' and row[2] == 'Pass')):
                                print('First')
                                print(f'p_prd_f_wgt = {p_prd_f_prior} - (0.2 * {p_prd_f_prior}*({tdur}/{n_mod})) + 0.2*({p_prd_f_cond}*({tdur}/{n_mod}))')
                                p_prd_f_wgt = p_prd_f_prior - (0.2 * p_prd_f_prior*(tdur/n_mod)) + (0.2*p_prd_f_cond*(tdur/n_mod))
                            elif ((row[3] == 'Highly effective' and row[2] == 'Fail') or
                                  (row[3] == 'Usually effective' and row[2] == 'Fail')):
                                print('Second')
                                print(f'p_prd_f_wgt = {p_prd_f_cond}')
                                p_prd_f_wgt = p_prd_f_cond
                            elif ((row[3] == 'Faily effective' and row[2] == 'Fail') or
                                  (row[3] == 'Highly ineffective' and row[2] == 'Fail')):
                                print('Third')
                                print(f'p_prd_f_wgt = 0.5 * {p_prd_f_prior} + 0.5 * {p_prd_f_cond}')
                                p_prd_f_wgt = 0.5 * p_prd_f_prior + 0.5 * p_prd_f_cond

                        # if isinstance(p_prd_f_wgt, complex):
                            # p_prd_f_wgt = p_prd_f_wgt.real
                        if row[5] == 'Yes':
                            p_prd_f_wgt = ""
                        else:
                            p_prd_f_wgt = float(p_prd_f_wgt)
                        print(f'p_prd_f_wgt = {p_prd_f_wgt}')
                        row.append(p_prd_f_wgt)

                        val = 1 - p_prd_f_wgt
                        ln = -math.log(val, E)
                        b_1 = (1/1.8)
                        try:
                            eta_updated = row[6] / (ln**b_1)
                        except ZeroDivisionError:
                            eta_updated = 0
                        eta_updated = float(eta_updated)
                        # if isinstance(eta_updated, complex):
                            # eta_updated = n_updated.real
                        eta_updated = format_decimal(eta_updated)
                        print(f'eta_updated = {eta_updated}')
                        row.append(eta_updated)
                        n_mod = eta_updated
                    save_case_five(row)
                    print('\n')

                    if row[5] == 'Yes':
                        inspc_date = row[1]
                RBI_assessment_date = data.get('RBI_assessment_date') #.date()
                t = (RBI_assessment_date - inspc_date).days / 365
                p_fod = 1-math.e**(-((t/n_mod)**1.8))
                print(f't = {t}')
                print(f'p_fod = {p_fod}')


                F_set = F_set_formula(data['Type_of_PRD'], data['PRD_set'], data['Operating_Pressure_of_the_Protected_Equipment'])
                print(f'F_set = {F_set}')


                if data['Rupture_disk_is_installed_upstream_of_PRD'] == 'no':
                    p_prd_l = p_fod * F_set
                else:
                    p_prd_l = 0
                print(f'p_prd_l = {p_prd_l}')





            if determine_case_six(objects_history_data):
                values = fetch_history_case_four()
                first_installation = GeneralInformation.objects.first() #first()
                first_installation = first_installation.Installation_of_PRD
                inspection_date = data['RBI_assessment_date']
                years = (inspection_date - first_installation).days / 365
                p_prd_f_prior = 0
                n_mod = n_mod_value
                t = 0
                eta_updated = 0
                n_updated = 0
                E = format_decimal(math.e)
                for row in values:
                    print(row)
                    print('\n')
                    tdur = format_decimal(row[6])
                    if row[3] == 'None':
                        p_prd_f_prior, p_prd_p_prior = '', ''
                        p_prd_f_cond, p_prd_f_wgt = '', ''
                        n_mod = n_mod_value
                        print(f'n_mod = {n_mod}')
                        n_updated = eta_updated
                        row.append(p_prd_f_prior)
                        row.append(p_prd_p_prior)
                        row.append(p_prd_f_cond)
                        row.append(p_prd_f_wgt)
                        row.append(eta_updated)
                    else:
                        if row[0] == 1:
                            try:
                                p_prd_f_prior = 1 - E**(-((tdur/n_mod)**1.8))
                            except ZeroDivisionError:
                                p_prd_f_prior = 0
                        else:
                            t = row[6]
                            p_prd_f_prior = 1 - E**(-((tdur/n_mod)**1.8))
                        p_prd_f_prior = format_decimal(p_prd_f_prior)
                        print(f'p_prd_f_prior = {p_prd_f_prior}')
                        p_prd_p_prior = 1 - p_prd_f_prior
                        p_prd_p_prior = format_decimal(p_prd_p_prior)
                        print(f'p_prd_p_prior = {p_prd_p_prior}')
                        row.append(p_prd_f_prior)
                        row.append(p_prd_p_prior)

                        p_prd_f_cond = 0
                        first, second = row[3].split(' ')
                        first = first.lower()
                        result = '_'.join([first, second])
                        cf_pass = CF['Inspection_Result']['leak'][result]
                        cf_fail = CF['Inspection_Result']['no_leak'][result]
                        if row[2] == 'Pass':
                            p_prd_f_cond = (1 - 0.7) * p_prd_p_prior
                        elif row[2] == 'Fail':
                            if row[2] == 'Fail' and row[3] == 'Highly effective':
                                p_prd_f_cond = 0.95 * p_prd_f_prior + (1 - 0.9) * p_prd_p_prior
                            else:
                                p_prd_f_cond = 0.95 * p_prd_f_prior + (1 - 0.7) * p_prd_p_prior

                        # if isinstance(p_prd_f_cond, complex):
                            # p_prd_f_cond = p_prd_f_cond.real
                        p_prd_f_cond = float('{:.9f}'.format(p_prd_f_cond))
                        print(f'p_prd_f_cond = {p_prd_f_cond}')
                        row.append(p_prd_f_cond)

                        if row[0] == 1:
                            if ((row[3] == 'Highly effective' and row[2] == 'Pass') or
                                (row[3] == 'Usually effective' and row[2] == 'Pass') or
                                (row[3] == 'Faily effective' and row[2] == 'Pass')):
                                p_prd_f_wgt = p_prd_f_prior - (0.2 * p_prd_f_prior*(tdur/n_mod)) + 0.2*(p_prd_f_cond*(tdur/n_mod))
                            elif ((row[3] == 'Highly effective' and row[2] == 'Fail') or
                                  (row[3] == 'Usually effective' and row[2] == 'Fail')):
                                p_prd_f_wgt = p_prd_f_cond
                            elif (row[3] == 'Faily effective' and row[2] == 'Fail'):
                                p_prd_f_wgt = 0.5 * p_prd_f_prior + 0.5 * p_prd_f_cond
                        else:
                            if ((row[3] == 'Highly effective' and row[2] == 'Pass') or
                                (row[3] == 'Usually effective' and row[2] == 'Pass') or
                                (row[3] == 'Faily effective' and row[2] == 'Pass')):
                                p_prd_f_wgt = p_prd_f_prior - 0.2 * p_prd_f_prior*(tdur/n_mod) + 0.2*(p_prd_f_cond*(tdur/n_mod))
                            elif ((row[3] == 'Highly effective' and row[2] == 'Fail') or
                                  (row[3] == 'Usually effective' and row[2] == 'Fail')):
                                p_prd_f_wgt = p_prd_f_cond
                            elif (row[3] == 'Faily effective' and row[2] == 'Fail'):
                                p_prd_f_wgt = 0.5 * p_prd_f_prior + 0.5 * p_prd_f_cond

                        # if isinstance(p_prd_f_wgt, complex):
                            # p_prd_f_wgt = p_prd_f_wgt.real
                        p_prd_f_wgt = format_decimal(p_prd_f_wgt)
                        print(f'p_prd_f_wgt = {p_prd_f_wgt}')
                        row.append(p_prd_f_wgt)

                        val = 1 - p_prd_f_wgt
                        ln = -math.log(val, E)
                        b_1 = (1/1.8)
                        try:
                            eta_updated = row[6] / (ln**b_1)
                        except ZeroDivisionError:
                            eta_updated = 0
                        # if isinstance(eta_updated, complex):
                            # eta_updated = n_updated.real
                        eta_updated = format_decimal(eta_updated)
                        print(f'eta_updated = {eta_updated}')
                        row.append(eta_updated)
                        n_mod = eta_updated
                    if row[4] == 'Yes':
                        years = (data['RBI_assessment_date'] - row[1]).days / 365
                    save_case_six(row)
                    print('\n')

                p_fod = 1-math.e**(-((years/n_mod)**1.8))
                print(f't = {years}')
                print(f'p_fod = {p_fod}')


                F_set = F_set_formula(data['Type_of_PRD'], data['PRD_set'], data['Operating_Pressure_of_the_Protected_Equipment'])
                print(f'F_set = {F_set}')


                if data['Rupture_disk_is_installed_upstream_of_PRD'] == 'no':
                    p_prd_l = p_fod * F_set
                else:
                    p_prd_l = 0
                print(f'p_prd_l = {p_prd_l}')



            # if (determine_case_three(objects_history_data)) is False:
            applicable_overpress_data_copy = []
            for row in applicable_overpress_data:
                print(row)
                demand_case = row[1] #.lower().replace(' ', '_')
                F_op_j = 0
                p_oj = float(row[2])
                p_set = float(data['PRD_set'])
                F_op_j = 0
                if (p_oj / p_set) < 1.3:
                    F_op_j = 1.0
                elif (float(p_oj) / float(p_set)) > 4.0:
                    F_op_j = 0.2
                else:
                    F_op_j = 1 - (1 / 3.375)*((p_oj/p_set)-1.3)


                print(f'F_op_j = {F_op_j}')
                row[-6] = F_op_j


                P_fod_j = p_fod * F_op_j
                print(f'P_fod_j = {P_fod_j}')
                row[-5] = P_fod_j

                EF_j_value = EF_j[demand_case]
                print(f'EF_j_value = {EF_j_value}')
                row[-4] = EF_j_value

                DRRF_j = DDRF_j[demand_case]
                print(f'DRRF_j = {DRRF_j}')
                row[-3] = DRRF_j

                DR_j = EF_j_value * DRRF_j
                print(f'DR_j = {DR_j}')

                row[-2] = DR_j
                save_overpressure_demand_case(row[:-1])
                applicable_overpress_data_copy.append(row)
                # print(applicable_overpress_data_copy)


                Df = float(DF_Class[data['Protected_Equipment_Demage_Status']])
                print(f'Df = {Df}')


                gff_total = 3.06e-05
                Fms = float(data['management_system_factor'])
                P_f_t = gff_total * Df * Fms
                print(f'P_f_t = {P_f_t}')

                MAWP = float(data['Maximum_Allow_able_Working_Pressure_of_Protected_Equipment'])
                P_f_j = (0.0312881 * gff_total * Df * Fms) * math.e**(3.464837 * (p_oj / MAWP))
                print(f'P_f_j = {P_f_j}')

                P_prd_f_j = P_fod_j * DR_j * P_f_j
                # if isinstance(P_prd_f_j, complex):
                    # P_prd_f_j = P_prd_f_j.real
                print(f'P_prd_f_j = {P_prd_f_j}')
                print('\n\n')









            # 1.3 PRD PROBABILITY OF LEAKAGE

            print('********** PRD PROBABILITY OF LEAKAGE **********')
            print('-' * 100)
            b_pol = 1.6
            print(f'b_pol = {b_pol}')

            n_def_pol_val = n_def_pol['fuild_severity'][data['Service_severity']][data['Type_of_PRD']]
            print(f'n_def_pol = {n_def_pol_val}')

            Fs_pol_val = Fs_POL(data['Type_of_PRD'], data['PRD_Containing_Soft_Seats'])
            print(f'Fs_pol = {Fs_pol_val}')

            F_env_pol_val = F_env_POL[data['Environment_Factor_Modifier']]
            print(f'f_env_pol = {F_env_pol_val}')

            n_mod_fod = Fs_pol_val * F_env_pol_val * n_def_pol_val
            print(f'n_mod_fod = {n_mod_fod}')





            if determine_case_two_leakage(objects_history_data):
                values = fetch_history_case_two_leakage()
                first_installation = GeneralInformation.objects.first()
                first_installation = first_installation.Installation_of_PRD
                inspection_date = data['RBI_assessment_date']
                years = (inspection_date - first_installation).days / 365
                years = float(f'{years:.9f}')
                p_prd_f_prior = 0
                n_mod = n_mod_fod
                t = 0
                eta_updated = 0
                for row in values:
                    print('\n')
                    if row[0] == 1:
                        try:
                            t = row[6]
                            p_prd_f_prior = 1 - math.e**(-((t/n_mod)**1.6))
                        except ZeroDivisionError:
                            p_prd_f_cond = 0
                    else:
                        t = row[6]
                        p_prd_f_prior = 1 - math.e**(-((t/n_mod)**1.6))
                    p_prd_f_prior = float('{:.9f}'.format(p_prd_f_prior))
                    print(f'p_prd_f_prior = {p_prd_f_prior}')
                    p_prd_p_prior = 1 - p_prd_f_prior
                    p_prd_p_prior = float('{:.9f}'.format(p_prd_p_prior))
                    print(f'p_prd_p_prior = {p_prd_p_prior}')
                    row.append(p_prd_f_prior)
                    row.append(p_prd_p_prior)

                    p_prd_f_cond = 0
                    result = ''
                    if row[3] == 'none':
                        result = row[3]
                    else:
                        first, second = row[3].split(' ')
                        first = first.lower()
                        result = '_'.join([first, second])
                    cf_pass = CF['Inspection_Result']['pass'][result]
                    print(f'cf_pass = {cf_pass}')
                    cf_fail = CF['Inspection_Result']['fail'][result]
                    print(f'cf_fail = {cf_fail}')
                    if row[2] == 'No leak':
                        p_prd_f_cond = (1 - cf_pass) * p_prd_p_prior
                    elif row[2] == 'Leak':
                        p_prd_f_cond = cf_fail * p_prd_f_prior + (1 - cf_pass) * p_prd_p_prior

                    # if isinstance(p_prd_f_cond, complex):
                        # p_prd_f_cond = p_prd_f_cond.real
                    p_prd_f_cond = float('{:.9f}'.format(p_prd_f_cond))
                    print(f'p_prd_f_cond = {p_prd_f_cond}')
                    row.append(p_prd_f_cond)

                    p_prd_f_wgt = 0
                    if ((row[3] == 'Highly effective' and row[2] == 'No leak') or
                        (row[3] == 'Usually effective' and row[2] == 'No leak') or
                        (row[3] == 'Faily effective' and row[2] == 'No leak')):
                        p_prd_f_wgt = p_prd_f_prior - (0.2 * p_prd_f_prior*(row[6]/n_mod)) + (0.2*(p_prd_f_cond*(row[6]/n_mod)))
                    elif ((row[3] == 'Highly effective' and row[2] == 'Leak') or
                          (row[3] == 'Usually effective' and row[2] == 'Leak')):
                        p_prd_f_wgt = p_prd_f_cond
                    elif (row[3] == 'Faily effective' and row[2] == 'Leak'):
                        p_prd_f_wgt = 0.5 * p_prd_f_prior + 0.5 * p_prd_f_cond

                    # if isinstance(p_prd_f_wgt, complex):
                        # p_prd_f_wgt = p_prd_f_wgt.real
                    p_prd_f_wgt = float('{:.9f}'.format(p_prd_f_wgt))
                    print(f'p_prd_f_wgt = {p_prd_f_wgt}')
                    row.append(p_prd_f_wgt)

                    val = 1 - p_prd_f_wgt
                    ln = -math.log(val, math.e)
                    b_1 = (1/1.6)
                    # try:
                    eta_updated = row[6] / (ln**b_1)
                    # except ZeroDivisionError:
                        # eta_updated = 0
                    # if isinstance(eta_updated, complex):
                        # eta_updated = n_updated.real
                    eta_updated = float('{:.9f}'.format(eta_updated))
                    print(f'eta_updated = {eta_updated}')
                    row.append(eta_updated)
                    save_case(row, 'case_two_leakage.csv')
                    n_mod = eta_updated
                    print(row)
                    print('\n')
                p_fod = 0.99235
                try:
                    p_fod = 1-math.e**(-((years/n_mod)**1.6))
                except ZeroDivisionError:
                    p_fod = 0.99235
                print(f't = {years}')
                print(f'p_pol = {p_fod}')


                F_set = F_set_formula(data['Type_of_PRD'], data['PRD_set'], data['Operating_Pressure_of_the_Protected_Equipment'])
                print(f'F_set = {F_set}')


                if data['Rupture_disk_is_installed_upstream_of_PRD'] == 'no':
                    p_prd_l = p_fod * F_set
                else:
                    p_prd_l = 0
                print(f'p_prd_l = {p_prd_l}')
                print('->' * 50)




            if determine_case_three_leakage(objects_history_data):
                values = fetch_history_case_two()
                RBI_assessment_date = data.get('RBI_assessment_date').date()
                t = 0
                insp = 0
                for row in values[0:2]:
                    insp = row[1]
                    t = (RBI_assessment_date - row[1]).days / 365
                p_fod = 1 - math.e**(-((t/n_mod_fod)**1.6))
                with open('case_three.csv', mode='a', newline='') as file:
                   writer = csv.writer(file)
                   writer.writerow([t, p_fod])
                print('\n\n')
                print(f'RBI date = {RBI_assessment_date}')
                print(f'Inspection test = {insp}')
                print(f't = {t}')
                print(f'p_prd_l_prior = {p_fod}')
                print('\n\n')

                F_set = F_set_formula(data['Type_of_PRD'], data['PRD_set'], data['Operating_Pressure_of_the_Protected_Equipment'])
                print(f'F_set = {F_set}')


                if data['Rupture_disk_is_installed_upstream_of_PRD'] == 'no':
                    p_prd_l = p_fod * F_set
                else:
                    p_prd_l = 0
                print(f'p_prd_l = {p_prd_l}')





            if determine_case_four_leakage(objects_history_data):
                values = fetch_history_case_two()
                p_prd_f_prior = 0
                n_mod = n_mod_fod
                t = 0
                inspc_date = 0
                eta_updated = 0
                for row in values:
                    print('\n')
                    if values[0][0] == 1:
                        t = row[6]
                        p_prd_f_prior = 1 - math.e**(-(t/n_mod)**1.6)
                    else:
                        p_prd_f_prior = 1 - math.e**(-(t/n_mod)**b)
                    print(f'p_prd_f_prior = {p_prd_f_prior}')
                    p_prd_p_prior = 1 - p_prd_f_prior
                    print(f'p_prd_p_prior = {p_prd_p_prior}')
                    row.append(p_prd_f_prior)
                    row.append(p_prd_p_prior)

                    p_prd_f_cond = 0
                    result = ''
                    if row[3] == 'none':
                        result = row[3]
                    else:
                        first, second = row[3].split(' ')
                        first = first.lower()
                        result = '_'.join([first, second])
                    cf_pass = CF['Inspection_Result']['pass'][result]
                    cf_fail = CF['Inspection_Result']['fail'][result]
                    if row[2] == 'Pass':
                        p_prd_f_cond = (1 - cf_pass) * p_prd_p_prior
                    elif row[2] == 'Fail':
                        p_prd_f_cond = cf_fail * p_prd_f_prior + (1 - cf_pass) * p_prd_p_prior

                    print(f'p_prd_f_cond = {p_prd_f_cond}')
                    row.append(p_prd_f_cond)


                    if values[0][0] == 1:
                        if ((row[3] == 'Highly effective' and row[2] == 'Pass') or
                            (row[3] == 'Usually effective' and row[2] == 'Pass') or
                            (row[3] == 'Faily effective' and row[2] == 'Pass')):
                            p_prd_f_wgt = p_prd_f_prior - 0.2 * p_prd_f_prior*(row[6]/n_mod) + 0.2*(p_prd_f_cond*(row[6]/n_mod))
                        elif ((row[3] == 'Highly effective' and row[2] == 'Fail') or
                              (row[3] == 'Usually effective' and row[2] == 'Fail')):
                            p_prd_f_wgt = p_prd_f_cond
                        elif (row[3] == 'Faily effective' and row[2] == 'Fail'):
                            p_prd_f_wgt = 0.5 * p_prd_f_prior + 0.5 * p_prd_f_cond
                    else:
                        if ((row[3] == 'Highly effective' and row[2] == 'Pass') or
                            (row[3] == 'Usually effective' and row[2] == 'Pass') or
                            (row[3] == 'Faily effective' and row[2] == 'Pass')):
                            p_prd_f_wgt = p_prd_f_prior - 0.2 * p_prd_f_prior*(row[6]/n_mod) + 0.2*(p_prd_f_cond*(row[6]/n_mod))
                        elif ((row[3] == 'Highly effective' and row[2] == 'Fail') or
                              (row[3] == 'Usually effective' and row[2] == 'Fail')):
                            p_prd_f_wgt = p_prd_f_cond
                        elif (row[3] == 'Faily effective' and row[2] == 'Fail'):
                            p_prd_f_wgt = 0.5 * p_prd_f_prior + 0.5 * p_prd_f_cond


                    # if isinstance(p_prd_f_wgt, complex):
                        # p_prd_f_wgt = p_prd_f_wgt.real
                    row.append(p_prd_f_wgt)
                    print(f'p_prd_f_wgt = {p_prd_f_wgt}')

                    val = 1 - p_prd_f_wgt
                    ln = -math.log(val, math.e)
                    b_1 = (1/1.6)
                    try:
                        eta_updated = row[6] / (ln**b_1)
                    except ZeroDivisionError:
                        eta_updated = 0
                    print(f'eta_updated = {eta_updated}')
                    n_mod = eta_updated
                    row.append(eta_updated)
                    save_case_four(row)
                    print('\n')
                    if row[4] == 'Yes':
                        inspc_date = row[1]
                RBI_assessment_date = data.get('RBI_assessment_date').date()
                t = (RBI_assessment_date - inspc_date).days / 365
                p_fod = 1-math.e**(-((t/n_mod)**1.8))
                print(f't = {t}')
                print(f'p_pol = {p_fod}')


                F_set = F_set_formula(data['Type_of_PRD'], data['PRD_set'], data['Operating_Pressure_of_the_Protected_Equipment'])
                print(f'F_set = {F_set}')


                if data['Rupture_disk_is_installed_upstream_of_PRD'] == 'no':
                    p_prd_l = p_fod * F_set
                else:
                    p_prd_l = 0
                print(f'p_prd_l = {p_prd_l}')



            if determine_case_five_leakage(objects_history_data):
                values = fetch_history_case_five()
                p_prd_f_prior = 0
                n_mod = n_mod_fod
                t = 0
                inspc_date = 0
                eta_updated = 0
                for row in values:
                    print('\n')
                    print(f'n_mod = {n_mod}')
                    if row[2] == 'None' and row[3] == 'None':
                        n_mod = n_mod_fod
                        inspc_date = row[1]
                        print(row)
                        print(n_mod)
                    else:
                    # if row[5] == 'Yes':
                    #     inspc_date = row[1]
                    # else:
                        if row[0] == 1:
                            t = row[6]
                            print(n_mod)
                            p_prd_f_prior = 1 - math.e**(-(t/n_mod)**1.6)
                        else:
                            print(n_mod)
                            t = row[6]
                            p_prd_f_prior = 1 - math.e**(-(t/n_mod)**1.6)
                        print(f'p_prd_f_prior = {p_prd_f_prior}')
                        p_prd_p_prior = 1 - p_prd_f_prior
                        print(f'p_prd_p_prior = {p_prd_p_prior}')
                        row.append(p_prd_f_prior)
                        row.append(p_prd_p_prior)

                        p_prd_f_cond = 0
                        result = ''
                        try:
                            first, second = row[3].split(' ')
                            first = first.lower()
                            result = '_'.join([first, second])
                        except ValueError:
                            result = row[3]
                        cf_pass = CF['Inspection_Result']['pass'][result]
                        cf_fail = CF['Inspection_Result']['fail'][result]
                        if row[2] == 'Pass':
                            p_prd_f_cond = (1 - cf_pass) * p_prd_p_prior
                        elif row[2] == 'Fail':
                            p_prd_f_cond = cf_fail * p_prd_f_prior + (1 - cf_pass) * p_prd_p_prior

                        row.append(p_prd_f_cond)
                        print(f'p_prd_f_cond = {p_prd_f_cond}')


                        if row[0] == 1:
                            if ((row[3] == 'Highly effective' and row[2] == 'Pass') or
                                (row[3] == 'Usually effective' and row[2] == 'Pass') or
                                (row[3] == 'Faily effective' and row[2] == 'Pass')):
                                print('First')
                                print(f'p_prd_f_wgt = {p_prd_f_prior} - 0.2 * {p_prd_f_prior}*({row[6]}/{n_mod}) + 0.2*({p_prd_f_cond}*({row[6]}/{n_mod}))')
                                p_prd_f_wgt = p_prd_f_prior - 0.2 * p_prd_f_prior*(row[6]/n_mod) + 0.2*(p_prd_f_cond*(row[6]/n_mod))
                            elif ((row[3] == 'Highly effective' and row[2] == 'Fail') or
                                  (row[3] == 'Usually effective' and row[2] == 'Fail')):
                                print('Second')
                                print(f'p_prd_f_wgt = {p_prd_f_cond}')
                                p_prd_f_wgt = p_prd_f_cond
                            elif (row[3] == 'Faily effective' and row[2] == 'Fail'):
                                print('Third')
                                print(f'p_prd_f_wgt = 0.5 * {p_prd_f_prior} + 0.5 * {p_prd_f_cond}')
                                p_prd_f_wgt = 0.5 * p_prd_f_prior + 0.5 * p_prd_f_cond
                        else:
                            if ((row[3] == 'Highly effective' and row[2] == 'Pass') or
                                (row[3] == 'Usually effective' and row[2] == 'Pass') or
                                (row[3] == 'Faily effective' and row[2] == 'Pass')):
                                print('First')
                                print(f'p_prd_f_wgt = {p_prd_f_prior} - 0.2 * {p_prd_f_prior}*({row[6]}/{n_mod}) + 0.2*({p_prd_f_cond}*({row[6]}/{n_mod}))')
                                p_prd_f_wgt = p_prd_f_prior - 0.2 * p_prd_f_prior*(row[6]/n_mod) + 0.2*(p_prd_f_cond*(row[6]/n_mod))
                            elif ((row[3] == 'Highly effective' and row[2] == 'Fail') or
                                  (row[3] == 'Usually effective' and row[2] == 'Fail')):
                                print('Second')
                                print(f'p_prd_f_wgt = {p_prd_f_cond}')
                                p_prd_f_wgt = p_prd_f_cond
                            elif (row[3] == 'Faily effective' and row[2] == 'Fail'):
                                print('Third')
                                print(f'p_prd_f_wgt = 0.5 * {p_prd_f_prior} + 0.5 * {p_prd_f_cond}')
                                p_prd_f_wgt = 0.5 * p_prd_f_prior + 0.5 * p_prd_f_cond


                        # if isinstance(p_prd_f_wgt, complex):
                            # p_prd_f_wgt = p_prd_f_wgt.real
                        row.append(p_prd_f_wgt)
                        print(f'p_prd_f_wgt = {p_prd_f_wgt}')

                        val = 1 - p_prd_f_wgt
                        ln = -math.log(val, math.e)
                        b_1 = (1/1.6)
                        try:
                            eta_updated = row[6] / (ln**b_1)
                        except ZeroDivisionError:
                            eta_updated = 0
                        n_mod = eta_updated
                        print(f'eta_updated = {eta_updated}')
                        row.append(eta_updated)
                        save_case_five(row)
                        print(row)
                        print(n_mod)
                        print('\n')


                RBI_assessment_date = data.get('RBI_assessment_date')
                t = (RBI_assessment_date - inspc_date).days / 365
                print(t)
                p_fod = 1-math.e**(-((t/n_mod)**1.6))
                print(f't = {t}')
                print(f'p_pol = {p_fod}')

                F_set = F_set_formula(data['Type_of_PRD'], data['PRD_set'], data['Operating_Pressure_of_the_Protected_Equipment'])
                print(f'F_set = {F_set}')


                if data['Rupture_disk_is_installed_upstream_of_PRD'] == 'no':
                    p_prd_l = p_fod * F_set
                else:
                    p_prd_l = 0
                print(f'p_prd_l = {p_prd_l}')



            if determine_case_six_leakage(objects_history_data):
                values = fetch_history_case_four()
                first_installation = GeneralInformation.objects.first() #first()
                first_installation = first_installation.Installation_of_PRD
                p_prd_f_prior = 0
                n_mod = n_mod_fod
                t = 0
                eta_updated = 0
                n_updated = 0
                years = 0
                E = format_decimal(math.e)
                for row in values:
                    print('\n')
                    print(row)
                    tdur = format_decimal(row[6])
                    if row[3] == 'None':
                        p_prd_l_prior, p_prd_p_prior = '', ''
                        p_prd_f_cond, p_prd_f_wgt = '', ''
                        n_mod = n_mod_fod
                        n_mod = n_mod_fod
                        row.append(p_prd_l_prior)
                        row.append(p_prd_p_prior)
                        row.append(p_prd_f_cond)
                        row.append(p_prd_f_wgt)
                        row.append(eta_updated)
                    else:
                        if row[0] == 1:
                            try:
                                p_prd_l_prior = 1 - E**(-((tdur/n_mod)**1.6))
                            except ZeroDivisionError:
                                p_prd_l_prior = 0
                        else:
                            t = row[6]
                            try:
                                p_prd_l_prior = 1 - E**(-((tdur/n_mod)**1.6))
                            except ZeroDivisionError:
                                p_prd_l_prior = 0.3
                        p_prd_l_prior = format_decimal(p_prd_l_prior)
                        print(f'p_prd_l_prior = {p_prd_l_prior}')
                        p_prd_p_prior = 1 - p_prd_l_prior
                        p_prd_p_prior = format_decimal(p_prd_p_prior)
                        print(f'p_prd_p_prior = {p_prd_p_prior}')
                        row.append(p_prd_l_prior)
                        row.append(p_prd_p_prior)

                        p_prd_f_cond = 0
                        first, second = row[3].split(' ')
                        first = first.lower()
                        result = '_'.join([first, second])
                        cf_pass = CF['Inspection_Result']['leak'][result]
                        cf_fail = CF['Inspection_Result']['no_leak'][result]
                        if row[2] == 'Pass':
                            p_prd_f_cond = (1 - 0.7) * p_prd_p_prior
                        elif row[2] == 'Fail':
                            if row[2] == 'Fail' and row[3] == 'Highly effective':
                                p_prd_f_cond = 0.95 * p_prd_l_prior + (1 - 0.9) * p_prd_p_prior
                            else:
                                p_prd_f_cond = 0.95 * p_prd_l_prior + (1 - 0.7) * p_prd_p_prior

                        # if isinstance(p_prd_f_cond, complex):
                            # p_prd_f_cond = p_prd_f_cond.real
                        p_prd_f_cond = float('{:.9f}'.format(p_prd_f_cond))
                        print(f'p_prd_f_cond = {p_prd_f_cond}')
                        row.append(p_prd_f_cond)

                        if row[0] == 1:
                            if ((row[3] == 'Highly effective' and row[2] == 'Pass') or
                                (row[3] == 'Usually effective' and row[2] == 'Pass') or
                                (row[3] == 'Faily effective' and row[2] == 'Pass')):
                                p_prd_f_wgt = p_prd_l_prior - (0.2 * p_prd_l_prior*(tdur/n_mod)) + 0.2*(p_prd_f_cond*(tdur/n_mod))
                            elif ((row[3] == 'Highly effective' and row[2] == 'Fail') or
                                  (row[3] == 'Usually effective' and row[2] == 'Fail')):
                                p_prd_f_wgt = p_prd_f_cond
                            elif (row[3] == 'Faily effective' and row[2] == 'Fail'):
                                p_prd_f_wgt = 0.5 * p_prd_l_prior + 0.5 * p_prd_f_cond
                        else:
                            if ((row[3] == 'Highly effective' and row[2] == 'Pass') or
                                (row[3] == 'Usually effective' and row[2] == 'Pass') or
                                (row[3] == 'Faily effective' and row[2] == 'Pass')):
                                p_prd_f_wgt = p_prd_l_prior - 0.2 * p_prd_l_prior*(tdur/n_mod) + 0.2*(p_prd_f_cond*(tdur/n_mod))
                            elif ((row[3] == 'Highly effective' and row[2] == 'Fail') or
                                  (row[3] == 'Usually effective' and row[2] == 'Fail')):
                                p_prd_f_wgt = p_prd_f_cond
                            elif (row[3] == 'Faily effective' and row[2] == 'Fail'):
                                p_prd_f_wgt = 0.5 * p_prd_l_prior + 0.5 * p_prd_f_cond

                        # if isinstance(p_prd_f_wgt, complex):
                            # p_prd_f_wgt = p_prd_f_wgt.real
                        p_prd_f_wgt = format_decimal(p_prd_f_wgt)
                        print(f'p_prd_f_wgt = {p_prd_f_wgt}')
                        row.append(p_prd_f_wgt)

                        val = 1 - p_prd_f_wgt
                        ln = -math.log(val, E)
                        b_1 = (1/1.6)
                        try:
                            eta_updated = row[6] / (ln**b_1)
                        except ZeroDivisionError:
                            eta_updated = 0
                        # if isinstance(eta_updated, complex):
                            # eta_updated = n_updated.real
                        eta_updated = format_decimal(eta_updated)
                        print(f'eta_updated = {eta_updated}')
                        row.append(eta_updated)
                        n_mod = eta_updated
                    if row[4] == 'Yes':
                        years = (data['RBI_assessment_date'] - row[1]).days / 365
                    save_case_six(row)
                    print('\n')

                try:
                    p_fod = 1-math.e**(-((years/n_mod)**1.6))
                except ZeroDivisionError:
                    p_fod = 0.3
                print(f't = {years}')
                print(f'p_fop = {p_fod}')

                F_set = F_set_formula(data['Type_of_PRD'], data['PRD_set'], data['Operating_Pressure_of_the_Protected_Equipment'])
                print(f'F_set = {F_set}')


                if data['Rupture_disk_is_installed_upstream_of_PRD'] == 'no':
                    p_prd_l = p_fod * F_set
                else:
                    p_prd_l = 0
                print(f'p_prd_l = {p_prd_l}')





            # if (determine_case_three(objects_history_data)) is False:
            applicable_overpress_data_copy = []
            DR_j_total = 0
            Risk_prd_f = 0
            C_prd_l = 0
            for row in applicable_overpress_data:
                demand_case = row[1].lower().replace(' ', '_')
                F_op_j = 0
                p_oj = float(row[2])
                p_set = float(data['PRD_set'])
                print(f'p_set = {p_set}')
                F_op_j = 0
                if (p_oj / p_set) < 1.3:
                    F_op_j = 1.0
                elif (float(p_oj) / float(p_set)) > 4.0:
                    F_op_j = 0.2
                else:
                    F_op_j = 1 - (1 / 3.375)*((p_oj/p_set)-1.3)

                print(f'\nF_op_j = {F_op_j}')
                row[-6] = F_op_j


                # P_fod_j = p_fod * F_op_j
                # if isinstance(P_fod_j, complex):
                    # P_fod_j = P_fod_j.real
                # print(f'P_fod_j = {P_fod_j}')
                # row[-5] = P_fod_j

                EF_j_value = EF_j[demand_case]
                print(f'EF_j_value = {EF_j_value}')
                row[-4] = EF_j_value

                DRRF_j = DDRF_j[demand_case]
                print(f'DRRF_j = {DRRF_j}')
                row[-3] = DRRF_j

                DR_j = EF_j_value * DRRF_j
                print(f'DR_j = {DR_j}')
                DR_j_total += DR_j

                row[-2] = DR_j
                save_overpressure_demand_case(row[:-1])
                applicable_overpress_data_copy.append(row)
                # print(applicable_overpress_data_copy)


                Df = float(DF_Class[data['Protected_Equipment_Demage_Status']])
                print(f'Df = {Df}')


                gff_total = 3.06e-05
                Fms = float(data['management_system_factor'])
                P_f_t = gff_total * Df * Fms
                print(f'P_f_t = {P_f_t}')

                print(f'gff_total = {gff_total}')
                print(f'p_oj = {p_oj}')
                print(f'Fms = {Fms}')
                print(f'MAWP = {MAWP}')
                MAWP = float(data['Maximum_Allow_able_Working_Pressure_of_Protected_Equipment'])
                P_f_j = (0.0312881 * gff_total * Df * Fms) * math.e**(3.464837 * (p_oj / MAWP))
                print(f'P_f_j = {P_f_j}')

                P_prd_f_j = P_fod_j * DR_j * P_f_j
                # if isinstance(P_prd_f_j, complex):
                    # P_prd_f_j = P_prd_f_j.real
                print(f'P_prd_f_j = {P_prd_f_j}')
                print('\n\n')



                # PRD COF TO OPEN ASSOCIATED WIHTHE Jth


                Fa = 0
                if data['Multiple_PRDs_protecting_fixed_equipment'] == 'Yes':
                    Fa = math.sqrt(float(data['Orifice_area_of_the_PRD']) / float(data['Total_installed_orifice_area_of_a_multiple_PDRs_installation']))
                else:
                    Fa = 1.0

                print(f'Fa  = {Fa}')

                p_o_j = 0
                if data['Multiple_PRDs_protecting_fixed_equipment'] == 'Yes':
                    p_o_j = float(Fa) * float(data['Overpressure_associated_with_the_overpressure'])
                else:
                    p_o_j = 1.0
                print(f'p_o_j = {p_o_j}')

                c_prd_f_j = float(data['PRD_COF_to_open_associated_with_jth_overpressure'])
                print(f'c_prd_f_j = {c_prd_f_j}')



                # PRD COF OF LEAKAGE


                W_c_prd = float(data['Rated_Capacity_of_PRD'])
                print(f'W_c_prd = {W_c_prd}')
                lrate_mild = 0.01 * W_c_prd
                print(f'lrate_mild = {lrate_mild}')

                lrate_so = 0.25 * W_c_prd
                print(f'lrate_so = {lrate_so}')

                D_mild_val = D_mild(data['PRD_Inlet_Size'], data['PRD_Discharge_Location'])
                print(f'D_mild = {D_mild_val}')

                D_so = 0.021
                print(f'D_so = {D_so}')

                Fr_value = Fr(data['PRD_Discharge_Location'])
                print(f'Fr_value = {Fr_value}')

                Cost_mild_inv = 24 * Fr_value * D_mild_val * float(data['Cost_of_the_fluid']) * lrate_mild
                print(f'Cost_mild_inv = {Cost_mild_inv}')


                Cost_so_inv = 24 * Fr_value * float(data['Cost_of_the_fluid']) * D_so * lrate_so
                print(f'Cost_so_inv = {Cost_so_inv}')


                C_env_value = float(C_env(data['PRD_Discharge_Location'], data['Environmental_clean_up_costs_due_to_a_PRD_leakage']))
                print(f'C_env = {C_env_value}')

                C_sd_value = float(C_sd(data['PRD_leakage_can_be_tolered'], data['Cost_of_shutdown_to_repair_PRD']))
                print(f'C_sd_value = {C_sd_value}')

                C_mild_prop = 0
                Unit_prod = float(data['Daily_production_margin_on_the_unit'])
                print(f'Unit_prod = {Unit_prod}')
                D_sd = float(data['Days_required_to_shutdown_a_unit_to_repair_a_leakage'])
                print(f'D_sd = {D_sd}')
                if data['PRD_leakage_can_be_tolered'] == 'yes':
                    C_mild_prop = 0
                elif data['PRD_leakage_can_be_tolered'] == 'no':
                    C_mild_prop = Unit_prod * D_sd

                print(f'C_mild_prop = {C_mild_prop}')

                Cost_so_prop = Unit_prod * D_sd
                print(f'Cost_so_prop = {Cost_so_prop}')

                C_mild_l = Cost_mild_inv + C_env_value + C_sd_value + C_mild_prop
                print(f'C_mild_l = {C_mild_l}')

                C_so_l = Cost_so_inv + C_env_value + C_sd_value + Cost_so_prop
                print(f'C_so_l = {C_so_l}')

                C_prd_l = (0.9 * C_mild_l) + (0.1 * C_so_l)
                print(f'C_prd_l = {C_prd_l}')



                # RISK FROM FAILURE TO OPEN

                Risk_prd_f_j = P_prd_f_j * c_prd_f_j
                print(f'Risk_prd_f_j = {Risk_prd_f_j}')

                Risk_prd_f += (P_prd_f_j * c_prd_f_j)
                print(f'Risk_prd_f = {Risk_prd_f}')



                # PRD RISK FROM LEAKAGE

            Risk_prd_l = p_prd_l * C_prd_l
            # if isinstance(Risk_prd_l, complex):
                # Risk_prd_l = Risk_prd_l.real
            print(f'Risk_prd_l = {Risk_prd_l}')


                # TOTAL RISK PRD

            Risk_prd = Risk_prd_f + Risk_prd_l
            print(f'Risk_prd = {Risk_prd}')

            # INSPECTION PLANNNG BASED ON RISK TARGETS



    else:
        print('The form is not valid!')

        # print()
        # print(data)


    save_inspec_histo_data(values)
    print(f'\n\nFirst case: {determine_case_one()}')
    print(f'Third case: {determine_case_three(objects_history_data)}')

    print(f'\nSecond case (POF): {determine_case_two(objects_history_data)}')
    print(f'Fourth case  (POF): {determine_case_four(objects_history_data)}')
    print(f'Fifth case  (POF): {determine_case_five(objects_history_data)}')
    print(f'Sixth case  (POF): {determine_case_six(objects_history_data)}')

    print(f'\nSecond case  (POL): {determine_case_two_leakage(objects_history_data)}')
    print(f'Third case  (POL): {determine_case_three_leakage(objects_history_data)}')
    print(f'Fourth case  (POL): {determine_case_four_leakage(objects_history_data)}')
    print(f'Fifth case  (POL): {determine_case_five_leakage(objects_history_data)}')
    print(f'Sixth case  (POL): {determine_case_six_leakage(objects_history_data)}')
    return render(request,
                  'webapp/Pages/prd_data.html',
                  {
                      'form_general': form_general,
                       'form_inspection': form_inspection,
                       'failure_to_open_form': failure_to_open_form,
                       'failure_of_leakage_form': failure_of_leakage_form,
                       'inspection_history': inspection_history,
                       'applicable_overpressure': applicable_overpressure,
                       'objects_history_data': objects_history_data,
                       'applicable_overpress_data': applicable_overpress_data,
                       'values': values
                   })




def prd_insp_history(request):
    form = Prd_InspectionHistoryForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            print(form.cleaned_data['RBI_inspection_test_date'])
            print(form.cleaned_data['PRD_pop_test_results'])
            print(form.cleaned_data['PRD_Leakage_results'])
        else:
            print('Form is not valid')
    return render(request,
                  'webapp/Pages/prd_inspection_history.html',
                  {'form': form})


def applicable_overpres_demand_case(request):
    applicable_overpressure = ApplicableOverpressureDemandCaseForm(request.POST)
    return render(request,
                  'webapp/Pages/applicable_overpres_demand.html',
                  {'applicable_overpressure': applicable_overpressure})

@login_required(login_url='/prd/login')
def prd_input_data(request):
    form_general = GeneralInformationForm(request.POST)
    form_inspection = PRD_InspectionForm(request.POST)
    failure_to_open_form = ConsequencesOfFailureInputDataForm(request.POST)
    failure_of_leakage_form = Consequences0fFailureOfLeakageForm(request.POST)
    applicable_overpressure_demand = ApplicableOverpressureDemandCaseForm()
    prd_inspection_history = Prd_InspectionHistoryForm()
    if request.method == 'POST':
        if failure_of_leakage_form.is_valid():
            # failure_of_leakage_form.save(commit=True)
            print(failure_of_leakage_form.cleaned_data)
        else:
            print('The form is not valid!')
    return render(request,
                  'webapp/Pages/prd_data.html',
                  {
                      'form_general': form_general,
                       'form_inspection': form_inspection,
                       'failure_to_open_form': failure_to_open_form,
                       'failure_of_leakage_form': failure_of_leakage_form,
                       'applicable_overpressure_demand': applicable_overpressure_demand,
                       'prd_inspection_history': prd_inspection_history
                   })


@login_required(login_url='/prd/login/')
def homepage(request):
    return render(request,
                  'webapp/Pages/homepage.html')


@login_required(login_url='/prd/login/')
def inspection_planning(request):
    return render(request,
                  'webapp/Pages/inspection_planning.html')

@login_required(login_url='/prd/login/')
def risk_assessment(request):
    return render(request,
                  'webapp/Pages/risk_assessment_results.html')

