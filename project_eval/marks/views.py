from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import Rubrics,Marks
from accounts.models import Student,Faculty, Team, Guide, Panel
from .utils import processStudentGuideForm,getStudentMarks,processStudentPanelForm,getCurrentPhaseMarks,processMarksUpdation,getPhaseData
from core.roles import isPanel,isGuide,isSuperUser
import xlwt
from django.db.models import Max

def enterStudentMarksGuide(request,usn,phase):
    template_name = 'marks/enter_student_marks_guide_eval.html'

    # authentication
    if (not isGuide(request.user)):
        return HttpResponse("you are not authorized to view this page!")

    student = Student.objects.get(usn=usn)
    rubrics = Rubrics.objects.filter(phase=phase)

    # check if marks have been previously assigned:
    if(len(Marks.objects.filter(usn=student,rubric_id=rubrics[0],faculty__in=Faculty.objects.filter(is_guide=True)))):
        return HttpResponse("marks have already been assigned for this student")

    is_intern = "Yes" if student.is_intern else "No"

    context = {
        "student":student,
        "rubrics":rubrics,
        "phase":phase,
        "is_intern":is_intern,
    }

    # handling post request:
    if(request.method == 'POST'):
        guide = request.user.guide.guide_faculties.all()[0]
        processStudentGuideForm(student,guide,rubrics,request.POST)
        return redirect('/dashboard')

    return render(request,template_name,context)

def updateStudentMarks(request,usn,phase):
    marks_obj,rubrics,student,marks = getCurrentPhaseMarks(usn,phase)
    context = {
        "marks":marks,
        "student":student,
        "rubrics":rubrics,
        "phase":phase,
    }

    if (not isSuperUser(request.user)):
        return HttpResponse("you are not authorized to view this page!")

    # handling post request:
    if(request.method == 'POST'):
        processMarksUpdation(marks_obj,request.POST)
        return redirect('/dashboard')

    template_name = 'marks/update_student_marks.html'
    return render(request,template_name,context)

def enterStudentMarksPanel(request,usn,phase):
    template_name = 'marks/enter_student_marks_panel_eval.html'

    # authentication
    if (not isPanel(request.user)):
        return HttpResponse("you are not authorized to view this page!")

    student = Student.objects.get(usn=usn)
    rubrics = Rubrics.objects.filter(phase=phase)
    panel_members = request.user.panel.panel_faculties.all()

    # check if marks have been previously assigned:
    if(len(Marks.objects.filter(usn=student,rubric_id=rubrics[0],faculty__in=Faculty.objects.filter(is_guide=False)))):
        return HttpResponse("marks have already been assigned for this student")


    context = {
        "student":student,
        "rubrics":rubrics,
        "panel":panel_members,
        "phase":phase,
    }

    if(request.method == 'POST'):
        processStudentPanelForm(student,rubrics,panel_members,request.POST)
        return redirect('/dashboard')  # TODO: need to add panel-dashboard url here

    return render(request,template_name,context)

def viewStudentMarks(request,usn):
    template_name = 'marks/view_student_marks.html'
    
    student = Student.objects.filter(usn=usn)    
    
    # TODO: authentication
    if(len(student) == 0):
        return HttpResponse("student does not exist! ")
    # handling a get request:

    student = student[0]
    data = getStudentMarks(student)

    context = {
        "student":student,
        "data":data,
    }

    return render(request,template_name,context)

def downloadPhaseMarks(request,phase):
    # authentication
    if (not isSuperUser(request.user)):
        return HttpResponse("you are not authorized to view this page!")

    # content-type of response
    response = HttpResponse(content_type='application/ms-excel')    
    
    #decide file name
    response['Content-Disposition'] = f'attachment;  filename="phase{phase}_report.xls"'   
    
    #creating workbook
    wb = xlwt.Workbook(encoding='utf-8')    
    
    #adding sheet
    ws = wb.add_sheet("sheet1") 
    font_style = xlwt.XFStyle()
    
    # headers are bold
    font_style.font.bold = True   
    
    #get your data, from database or from a text file...
    columns,data = getPhaseData(phase)  
    
    # Sheet header, first row
    row_num = 0 
    
    #write column headers in sheet
    for col_num in range(len(columns)):
    	ws.write(row_num, col_num, columns[col_num], font_style)    
    
    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    for row in data:
        row_num = row_num + 1
        for i,colm in enumerate(row):
            if(colm != -1):
                ws.write(row_num, i, colm, font_style) 
            else:
                ws.write(row_num, i, "", font_style)

    wb.save(response)
    return response

def downloadAllPhaseMarks(request):
    # authentication
    if (not isSuperUser(request.user)):
        return HttpResponse("you are not authorized to view this page!")

    # content-type of response
    response = HttpResponse(content_type='application/ms-excel')    
    
    #decide file name
    response['Content-Disposition'] = 'attachment; filename="final_eval_report.xls"'   
    
    #creating workbook
    wb = xlwt.Workbook(encoding='utf-8')    

    num_phases = Rubrics.objects.aggregate(Max('phase'))['phase__max']

    for phase in range(num_phases):
        #adding sheet
        ws = wb.add_sheet(f"sheet{phase+1}") 
        font_style = xlwt.XFStyle()
        
        # headers are bold
        font_style.font.bold = True  
        
        #get your data, from database or from a text file...
        columns,data = getPhaseData(phase + 1)  
        
        # Sheet header, first row
        row_num = 0 
        
        #write column headers in sheet
        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], font_style)    
        
        # Sheet body, remaining rows
        font_style = xlwt.XFStyle()

        for row in data:
            row_num = row_num + 1
            for i,colm in enumerate(row):
                if(colm != -1):
                    ws.write(row_num, i, colm, font_style) 
                else:
                    ws.write(row_num, i, "", font_style)

    wb.save(response)

    return response