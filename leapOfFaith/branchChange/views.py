from django.shortcuts import render
from django.http import HttpResponse
from branchChange.models import *
from django.forms.models import *
from django.shortcuts import *
from django.core.urlresolvers import reverse
from django.contrib import auth
from django.contrib.auth import logout
import csv
import os
# Create your views here.


def login(request):
    username = None
    if request.user.is_authenticated():
        username = request.user.username
        return HttpResponseRedirect('/branchChange/' + username)
    else:
        return render(request, 'branchChange/login.html')
    # if(is_authenticated):
    # 	return HttpResponseRedirect('profile')
    # else:


def login_request(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/')

    ldap = request.POST.get("ldap")
    password = request.POST.get("password")
    ldaperror = ""
    pwderror = ""
    context = {
        'ldap': ldap,
        'ldaperror': ldaperror,
        'pwd': password,
        'pwderror': pwderror
    }

    if (ldap == "admin"):
        if (password == "admin"):
            user = auth.authenticate(username="admin", password="admin")
            auth.login(request, user)
            return HttpResponseRedirect('/branchChange/admin')
        else:
            pwderror = "Username and Password do not match"
            context = {
                'ldap': ldap,
                'ldaperror': ldaperror,
                'pwd': password,
                'pwderror': pwderror
            }
            return render(request, 'branchChange/login.html', context)

    # username = get_object_or_404(Profile, roll=ldap)

    try:
        username = Profile.objects.get(roll=ldap)
    except Profile.DoesNotExist:
        username = None
        ldaperror = "User Does Not Exist"
        context = {
            'ldap': ldap,
            'ldaperror': ldaperror,
            'pwd': password,
            'pwderror': pwderror
        }
        return render(request, 'branchChange/login.html', context)

    user = auth.authenticate(username=username.user.username,
                             password=password)

    if user is None:
        pwderror = "Username and Password do not match"
        context = {
            'ldap': ldap,
            'ldaperror': ldaperror,
            'pwd': password,
            'pwderror': pwderror
        }
        return render(request, 'branchChange/login.html', context)
    else:
        auth.login(request, user)
        return HttpResponseRedirect('/branchChange/' + str(username.roll))


def register(request):
    username = None
    if request.user.is_authenticated():
        username = request.user.username
        return HttpResponseRedirect('/branchChange/' + username)
    programs = Program.objects.all()
    return render(request, 'branchChange/register.html',
                  {'programs': programs})


# def register_request(request):
# 	# if(is_authenticated):
# 	# 	return HttpResponseRedirect('profile')
# 	# else:
# 	roll = request.POST.get('roll')
# 	rollerror = "Fill valid name" if roll != '' else ''
# 	category = request.POST.get('category')
# 	categoryerror = "Fill Valid Category" if category != '' else ''
# 	name = request.POST.get('name')
# 	nameerror = "Fill Valid Name" if name != '' else ''
# 	password = request.POST.get('password')
# 	passworderror = "Fill Valid Password" if password != '' else ''
# 	branch = request.POST.get('branch')
# 	brancherror = "Fill Valid Branch" if branch != '' else ''

# 	cpi = request.POST.get('cpi')
# 	cpi = float(cpi)
# 	if (cpi == '' or cpi<0 or cpi > 10):
# 		cpierror = "Enter Valid CPI between 0 and 10"
# 	else:
# 		cpierror = ''

# 	context = {'roll': roll, 'rollerror': rollerror, 'category': category, 'categoryerror': categoryerror, 'name': name, 'nameerror': nameerror, 'password': password, 'passworderror': passworderror, 'branch': branch, 'brancherror': brancherror, 'cpi': cpi, 'cpierror': cpierror}

# 	error = False
# 	for k,v in context.items():
# 		if (v == ''):
# 			error = True
# 	if (float(context['cpi'])>10.0):
# 	# if (0 < -1):
# 		error = True
# 	if error:
# 		return render(request, 'branchChange/register.html', context)
# 	else:
# 		return HttpResponseRedirect(reverse('branchChange:profile', args=(usr.roll,)))


# def profile(request, roll_no):
# 	usr = get_object_or_404(Profile, roll=roll_no)
# 	branch = usr.allotted
# 	preferences = []
# 	for p in usr.preferences.all():
# 		if(p and p.name!="" and p.name!=branch.name):
# 			preferences.append(p)
#
# 	context = {'user': usr, 'current_branch': branch, 'preferences': preferences}
# 	return render(request, 'branchChange/profile.html', context)
def register_request(request):
    username = None
    if request.user.is_authenticated():
        username = request.user.username
        return HttpResponseRedirect('/branchChange/' + username)
    error = False

    roll = request.POST.get('roll')
    if not (roll.isdigit() and len(roll) == 9 and roll[0:2] == "15"):
        rollerror = "Enter Valid Roll Number 15xxxxxxx"
        error = True
    else:
        rollerror = ''

    category = request.POST.get('category')
    if not (category == 'GE' or category == 'SC' or category == 'ST'
            or category == 'OBC' or category == 'PwD'):
        categoryerror = "Fill valid category"
        error = True
    else:
        categoryerror = ''

    name = request.POST.get('name')
    if not (name.isalpha()):
        nameerror = "Fill valid name"
        error = True
    else:
        nameerror = ''

    password = request.POST.get('password')
    if password == '':
        passworderror = "Fill Valid Password"
        error = True
    elif len(password) < 5 or len(password) > 20:
        passworderror = "Password must be betwen 5 and 20 characters"
        error = True
    else:
        passworderror = ''

    branch = request.POST.get('branch')
    prog = None
    try:
        prog = Program.objects.get(name=branch)
    except Program.DoesNotExist:
        prog = None

    if prog is not None:
        brancherror = ''
    else:
        brancherror = "Fill Valid Branch"
        error = True

    cpi = request.POST.get('cpi')
    try:
        cpi = float(cpi)
    except ValueError:
        cpierror = "Enter Valid CPI between 0 and 10"

    if (cpi == '' or cpi < 0 or cpi > 10.0):
        cpierror = "Enter Valid CPI between 0 and 10"
        error = True
    else:
        cpierror = ''

    programs = Program.objects.all()
    context = {
        'programs': programs,
        'roll': roll,
        'rollerror': rollerror,
        'category': category,
        'categoryerror': categoryerror,
        'name': name,
        'nameerror': nameerror,
        'password': password,
        'passworderror': passworderror,
        'branch': branch,
        'brancherror': brancherror,
        'cpi': cpi,
        'cpierror': cpierror
    }

    if error:
        return render(request, 'branchChange/register.html', context)
    else:
        usr = User.objects.create_user(roll, roll + '@iitb.ac.in', password)
        usr.save()
        profile = Profile.objects.create(user=usr,
                                         roll=roll,
                                         name=name,
                                         cpi=cpi,
                                         allotted=prog,
                                         category=category)
        user = auth.authenticate(username=usr.username, password=password)
        auth.login(request, user)

        return HttpResponseRedirect('/branchChange/' + str(roll))


def profile(request, roll_no):
    username = None
    if request.user.is_authenticated():
        username = request.user.username
        if not (username == roll_no) or username == "admin":
            return HttpResponseRedirect('/')
    else:
        return HttpResponseRedirect('/')

    usr = get_object_or_404(Profile, roll=roll_no)
    branch = usr.allotted
    preferences = []
    prgs = ProgramProfile.objects.all().filter(
        student__user__username=usr.user.username)
    prgs = prgs.order_by('number')
    # prgs.sort(key=lambda x: x.number)
    for p in prgs:
        p_program = p.program
        if (p_program and p_program.name != ""
                and p_program.name != branch.name):
            preferences.append(p_program)

    context = {
        'user': usr,
        'current_branch': branch,
        'preferences': preferences
    }
    return render(request, 'branchChange/profile.html', context)


def update_pref(request, roll_no):
    username = None
    if request.user.is_authenticated():
        username = request.user.username
        if not (username == roll_no) or username == "admin":
            return HttpResponseRedirect('/')
    else:
        return HttpResponseRedirect('/')

    usr = get_object_or_404(Profile, roll=roll_no)
    branch = usr.allotted

    preferences = []
    prgs = ProgramProfile.objects.all().filter(
        student__user__username=usr.user.username)
    prgs = prgs.order_by('number')
    # prgs.sort(key=lambda x: x.number)
    for p in prgs:
        p_program = p.program
        if (p_program and p_program.name != ""
                and p_program.name != branch.name):
            preferences.append(p_program)

            # p = get_object_or_404(Program, name=pref)
            # 		new_pref = ProgramProfile.objects.create(student = usr, program = p, number = i)
            # 		i = i+1
            # 		pp = ProgramProfile.objects.create(student = usr, program = p, number = len(usr.preferences.all()))
            # 		usr.preferences.add(new_pref)

    total = len(preferences)
    total += 1

    pr = Program(name="", sanctioned=0, current=0)
    for x in range(len(preferences), 14):
        preferences.append(pr)

    programmes = Program.objects.all()
    context = {
        'user': usr,
        'current_branch': branch,
        'preferences': preferences,
        'programmes': programmes,
        'total': total
    }
    return render(request, 'branchChange/update_preferences.html', context)


def allUnique(x):
    seen = set()
    return not any(i in seen or seen.add(i) for i in x)


def save(request, roll_no):
    username = None
    if request.user.is_authenticated():
        username = request.user.username
        if not (username == roll_no) or username == "admin":
            return HttpResponseRedirect('/')
    else:
        return HttpResponseRedirect('/')

    usr = get_object_or_404(Profile, roll=roll_no)
    branch = usr.allotted
    # preferences = []
    # for p in usr.preferences.all():
    # 	if(p and p.name!="" and p.name!=branch.name):
    # 		preferences.append(p)

    total = 0
    empty_started = False
    error1_given = False
    error2_given = False
    errors = ""
    entered_prefs = []
    for i in range(1, 14):
        get_val = request.POST.get("sel" + str(i))
        if (not (get_val == "") and (get_val in entered_prefs)):
            errors += "Please Enter Unique Preferences\n"
            error2_given = True

        entered_prefs.append(get_val)

        if (empty_started and not (entered_prefs[-1] == "")):
            errors += "Dont leave intermediate branches empty\n"
            error1_given = True
        if (entered_prefs[-1] == ""):
            empty_started = True
        else:
            total = min(i + 1, total)

        if (entered_prefs[-1] == branch.name):
            errors += "You cant select allotted branch as a Preference\n"

    # for x in range(1,14):
    # 	entered_prefs[x] = request.POST["sel"+str(x)]
    programmes = Program.objects.all()
    context = {
        'user': usr,
        'current_branch': branch,
        'preferences': entered_prefs,
        'programmes': programmes,
        'total': total,
        'errors': errors
    }
    # context = {'user': usr, 'current_branch': branch, 'preferences': preferences, 'programmes': programmes, 'total': total}
    if (errors == ""):
        # usr.preferences.clear()
        user_pref = ProgramProfile.objects.all().filter(
            student__user__username=usr.user.username).values_list("id",
                                                                   flat=True)
        ProgramProfile.objects.exclude(pk__in=list(user_pref)).delete()

        i = 1
        for pref in entered_prefs:
            pref = pref.encode('ascii', 'ignore')
            if (pref):
                if (not pref == ""):
                    p = get_object_or_404(Program, name=pref)
                    pp = ProgramProfile.objects.create(student=usr,
                                                       program=p,
                                                       number=i)
                    i += 1

        usr.save()
        return HttpResponseRedirect('/branchChange/' + str(roll_no))
    else:
        return render(request, 'branchChange/update_preferences.html', context)


def admin(request):
    username = None
    if request.user.is_authenticated():
        username = request.user.username
        if not (username == "admin"):
            return HttpResponseRedirect('/')
    else:
        return HttpResponseRedirect('/')

    return render(request, 'branchChange/admin.html')


def handle_uploaded_file(f, name):
    with open('branchChange/' + name, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)


def algo():
    alpha = 0.75
    beta = 1.1

    import csv

    class Program:
        def __init__(self, name, sanctioned, original):
            self.name = name
            sanctioned = int(sanctioned)
            original = int(original)
            self.sanctioned = sanctioned
            self.original = original
            self.current = original
            self.min = round(sanctioned * alpha)  #HAVE A LOOK
            self.max = round(sanctioned * beta)
            self.blocked = False
            self.bcpi = 0.00
            self.cutoff = 11.00

    class Student:
        def __init__(self, name, roll, cpi, branch, category, preferences):
            self.name = name
            self.roll = roll
            cpi = float(cpi)
            self.cpi = cpi
            self.category = category
            self.original_branch = branch
            self.alloted_branch = branch
            self.preferences = list(preferences)
            self.eligible = True
            if (category == 'GE' and cpi < 8.00):
                self.eligible = False
            if (category != 'GE' and cpi < 7.00):
                self.eligible = False

    programs = []
    with open('branchChange/input_programmes.csv', 'rb') as csvfile:
        rows = csv.reader(csvfile, delimiter=',')
        for row in rows:
            programs.append(Program(row[0], row[1], row[2]))

    students = []
    with open('branchChange/input_options.csv', 'rb') as csvfile:
        rows = csv.reader(csvfile, delimiter=',')
        for row in rows:
            pref, i = [], 5
            while (i < 20 and row[i] != ''):
                pref.append(row[i])
                i += 1
            students.append(
                Student(row[1], row[0], row[3], row[2], row[4], pref))

    students.sort(key=lambda student: student.cpi, reverse=True)

    def find_program(name, programs):
        return [x for x in programs if x.name == name][0]

    update = True
    while (update):
        update = False
        for student in students:
            if (student.eligible):
                moved = False
                for pref in student.preferences:
                    if (pref == student.alloted_branch):
                        break
                    if (not moved):
                        dprog = find_program(pref, programs)
                        if (((not dprog.blocked)
                             or (dprog.blocked and student.cpi > dprog.bcpi))):
                            if (student.cpi >= dprog.cutoff):

                                curr = find_program(student.alloted_branch,
                                                    programs)
                                curr.current -= 1
                                dprog.current += 1
                                student.alloted_branch = dprog.name
                                moved = True
                                update = True
                                dprog.cutoff = min(dprog.cutoff, student.cpi)
                            elif ((student.cpi >= 9)
                                  or (student.cpi < 9
                                      and dprog.current >= dprog.min)):
                                if (dprog.current < dprog.max):

                                    curr = find_program(
                                        student.alloted_branch, programs)
                                    curr.current -= 1
                                    dprog.current += 1
                                    student.alloted_branch = dprog.name
                                    moved = True
                                    update = True
                                    dprog.cutoff = min(dprog.cutoff,
                                                       student.cpi)
            for pref in student.preferences:
                if (pref != student.alloted_branch):
                    dprog = find_program(pref, programs)
                    dprog.blocked = True
                    dprog.bcpi = max(dprog.bcpi, student.cpi)
                else:
                    break

        for prog in programs:
            prog.blocked = False
            prog.bcpi = 0.00

    output_stats = []
    for prog in programs:
        nrow = {
            'Program': prog.name,
            'Cutoff': prog.cutoff,
            'Santioned Strength': prog.sanctioned,
            'Original Strength': prog.original,
            'Final Strength': prog.current
        }
        if (nrow['Cutoff'] == 11):
            nrow['Cutoff'] = 'NA'
        output_stats.append(nrow)

    writer = csv.DictWriter(open('branchChange/output_stats.csv', 'w'),
                            delimiter=',',
                            fieldnames=[
                                'Program', 'Cutoff', 'Santioned Strength',
                                'Original Strength', 'Final Strength'
                            ])
    writer.writerows(output_stats)

    allotment = []
    for student in students:
        nrow = {
            'Roll': student.roll,
            'Name': student.name,
            'Original': student.original_branch,
            'Alloted': student.alloted_branch
        }
        if (nrow['Original'] == nrow['Alloted']):
            nrow['Alloted'] = "Branch Unchanged"
        if (not student.eligible):
            nrow['Alloted'] = "Ineligible"
        allotment.append(nrow)
    # filename = os.path('branchChange/allotment.csv')
    try:
        os.remove('branchChange/allotment.csv')
    except OSError:
        pass
    writer = csv.DictWriter(open('branchChange/allotment.csv', 'w'),
                            delimiter=',',
                            fieldnames=['Roll', 'Name', 'Original', 'Alloted'])
    writer.writerows(allotment)


def Upload(request):
    username = None
    if request.user.is_authenticated():
        username = request.user.username
        if not (username == "admin"):
            return HttpResponseRedirect('/')
    else:
        return HttpResponseRedirect('/')

    if request.method == 'POST':
        handle_uploaded_file(request.FILES['options'], "input_options.csv")
        handle_uploaded_file(request.FILES['programmes'],
                             "input_programmes.csv")
    algo()

    Program.objects.all().delete()
    Profile.objects.all().delete()
    ProgramProfile.objects.all().delete()
    u = User.objects.all()
    u = u.exclude(id=1)
    u.delete()

    with open('branchChange/input_programmes.csv', 'rb') as csvfile:
        rows = csv.reader(csvfile, delimiter=',')
        for row in rows:
            nprogram = Program.objects.create(name=row[0],
                                              sanctioned=row[1],
                                              current=row[2])

    with open('branchChange/input_options.csv', 'rb') as csvfile:
        rows = csv.reader(csvfile, delimiter=',')
        for row in rows:
            pref, i = [], 5
            usr = User.objects.create_user(row[0] + row[1] + row[3],
                                           row[1] + "@iitb.ac.in", row[1])
            usr.save()
            aloted = get_object_or_404(Program, name=row[2])
            nstud = Profile(user=usr,
                            roll=row[0],
                            name=row[1],
                            cpi=row[3],
                            allotted=aloted)
            nstud.save()
            while (i < 20 and row[i] != ''):
                p = get_object_or_404(Program, name=row[i])
                # nstud.preferences.add(p)
                pp = ProgramProfile.objects.create(student=nstud,
                                                   program=p,
                                                   number=(i - 4))
                # nstud.save()
                i += 1

            # name, roll, cpi, branch, category, preferences

            # students.append(Student(row[1], row[0], row[3], row[2], row[4], pref))

    return HttpResponseRedirect('/branchChange/admin')


def download(request):
    username = None
    if request.user.is_authenticated():
        username = request.user.username
        if not (username == "admin"):
            return HttpResponseRedirect('/')
    else:
        return HttpResponseRedirect('/')

    fsock = open('branchChange/allotment.csv', 'r')
    response = HttpResponse(fsock, content_type='text/csv')
    response['Content-Disposition'] = "attachment; filename=allotment.csv"
    return response


import operator


def idownload(request):
    username = None
    if request.user.is_authenticated():
        username = request.user.username
        if not (username == "admin"):
            return HttpResponseRedirect('/')
    else:
        return HttpResponseRedirect('/')

    all_users = Profile.objects.all()
    csv_output = []
    for user in all_users:
        row = []
        row.append(user.roll)
        row.append(user.name)
        row.append(user.allotted.name)
        row.append(user.cpi)
        row.append(user.category)
        i = 5
        prgs = ProgramProfile.objects.all().filter(
            student__user__username=user.user.username)
        prgs = prgs.order_by('number')
        # prgs.sort(key=lambda x: x.number)
        for p in prgs:
            p_program = p.program
            row.append(p_program.name)
            i += 1
        while (i < 20):
            row.append("")
            i += 1
        csv_output.append(row)

    with open("branchChange/input_options.csv", "w") as f:
        writer = csv.writer(f)
        writer.writerows(csv_output)

    fsock = open('branchChange/input_options.csv', 'r')
    response = HttpResponse(fsock, content_type='text/csv')
    response['Content-Disposition'] = "attachment; filename=input_options.csv"
    return response


def log_out(request, roll_no):
    logout(request)
    return HttpResponseRedirect('/')
