from .models import Marks, Rubrics
from accounts.models import Faculty, Team, Student, Panel


def processStudentGuideForm(usn, guide, rubrics, data):
    for i in rubrics:
        marks = data.get(str(i.id))
        m = Marks.objects.create(usn=usn, rubric_id=i,
                                 marks=marks, faculty=guide)
        m.save()


def processStudentPanelForm(student, rubrics, panel, data):
    for panel_member in panel:
        for rubric in rubrics:
            key = str(rubric.id)+'_'+str(panel_member.id)
            m = Marks.objects.create(
                usn=student, rubric_id=rubric, marks=data.get(key), faculty=panel_member)
            m.save()


def getStudentMarks(student):
    """
        the structure of the returned data is as follows (forgive me for this messy section):
        data = [
            {
                #<--- rubrics object belonging to a particular phase
                "rubrics":[r1,r2,r3],
                "marks":[
                    {
                        #<--- marks assigned by faculty
                        "marks":[r1_m,r2_m,...],
                        "faculty":faculty_q_set,
                    },
                    {
                        "marks":[r1_m,r2_m,...],
                        "faculty":faculty_q_set,
                    },
                    .
                    .
                    .

                ],                              #<--- marks scored for each rubric assigned by each
                                                     panel member(m1,m2,m3 are arrays)
                                                     (-1 if no marks have been allocated)
                "faculty_members":[p1,p2,p3..]  #<--- list of panel members
                "phase_number":p,               #<--- phase number
            },
            ...dictionaries similar to the one above are repeated for different phases
        ]
    """

    marks_q_set = student.marks
    rubrics_q_set = Rubrics.objects.all()
    no_faculty_members = len(Panel.objects.all()[0].panel_faculties.all()) + 1
    if(student.is_intern):
        no_faculty_members += 1

    rubrics_organized = {}
    for i in rubrics_q_set:
        if(i.phase not in rubrics_organized.keys()):
            rubrics_organized[i.phase] = [i]
        else:
            rubrics_organized[i.phase].append(i)

    rubrics = []
    for key in rubrics_organized.keys():
        rubrics.append(rubrics_organized[key])

    marks_temp = []
    faculty_members = []
    for phase in rubrics:
        temp = []
        for rubric in phase:
            query = marks_q_set.filter(rubric_id=rubric.id)
            if(len(query) == 0):
                temp.append([-1 for i in range(no_faculty_members)])
                faculty_members_temp = [-1 for i in range(no_faculty_members)]
            elif(len(query) == no_faculty_members):
                temp.append([q.marks for q in query])
                faculty_members_temp = [q.faculty for q in query]
            elif(len(query) == 1):
                guide_marks = [q.marks for q in query]
                panel_marks = [-1 for i in range(no_faculty_members-1)]
                temp.append(panel_marks + guide_marks)
                guide = [q.faculty for q in query]
                panel_members = [-1 for i in range(no_faculty_members - 1)]
                faculty_members_temp = panel_members + guide
            else:
                guide_marks = [-1]
                panel_marks = [q.marks for q in query]
                temp.append(panel_marks + guide_marks)
                guide = [-1]
                panel_members = [q.faculty for q in query]
                faculty_members_temp = panel_members + guide

        marks_temp.append(temp)
        faculty_members.append(faculty_members_temp)

    # dont touch this!!!
    marks = []
    for i in range(len(marks_temp)):
        tp1 = []
        for k in range(no_faculty_members):
            tp2 = []
            for j in range(len(marks_temp[i])):
                tp2.append(marks_temp[i][j][k])
            tp1.append({"marks": tp2, "faculty": list(faculty_members)[i][k]})
        marks.append(tp1)

    data = []
    for i in range(len(rubrics)):
        data.append({"rubrics": rubrics[i], "marks": marks[i],
                    "faculty_members": faculty_members[i], "phase_number": rubrics[i][0].phase})

    return data


def getCurrentPhaseMarks(usn, phase):
    student = Student.objects.get(usn=usn)
    rubrics = Rubrics.objects.filter(phase=phase)
    marks_obj = Marks.objects.filter(
        usn=usn, rubric_id__in=[i.id for i in rubrics])

    faculty_members = []
    for m in marks_obj.filter(rubric_id=rubrics[0].id):
        faculty_members.append(m.faculty)

    marks = []
    for f in faculty_members:
        temp = {
            "faculty_member": f,
            "marks": [],
        }
        for i in rubrics:
            m = marks_obj.get(rubric_id=i.id, faculty=f.id)
            temp["marks"].append(
                {"marks": m.marks, "max_marks": i.max_marks, "id": m.id})
        marks.append(temp)

    return (marks_obj, rubrics, student, marks)


def processMarksUpdation(marks, data):
    for mark_obj in marks:
        key = str(mark_obj.id)
        mark_obj.marks = data.get(key)
        mark_obj.save()


def getPhaseData(phase):
    students = Student.objects.all().order_by('usn')
    rubrics = Rubrics.objects.filter(phase=phase)
    no_panel_members = len(Panel.objects.all()[0].panel_faculties.all())

    columns = ["Name", "USN"]
    for i in range(no_panel_members):
        for rubric in rubrics:
            columns.append(f'pm{i+1}_{rubric.description}')

    for rubric in rubrics:
        columns.append(f'internal_guide_{rubric.description}')

    rub_id = []
    for rubric in rubrics:
        columns.append(f'external_guide_{rubric.description}')
        rub_id.append(rubric.id)

    data = []
    for student in students:
        student_marks = [student.full_name, student.usn]
        marks = student.marks
        int_guide = student.member.int_guide.guide_faculties.all()
        ext_guide = -1
        if(student.is_intern):
            ext_guide = student.member.ext_guide.guide_faculties.all()
            panel_marks = marks.exclude(
                faculty__in=[ext_guide[0], int_guide[0]])
        else:
            panel_marks = marks.exclude(faculty=int_guide[0])

        panel_members = []
        for m in panel_marks:
            if(m.faculty not in panel_members):
                panel_members.append(m.faculty)

        for pm in panel_members:
            for r_id in rub_id:
                try:
                    m = panel_marks.get(rubric_id=r_id, faculty=pm)
                    m = m.marks
                except Marks.DoesNotExist:
                    m = -1
                student_marks.append(m)

        for r_id in rub_id:
            try:
                m = marks.get(rubric_id=r_id, faculty=int_guide[0])
                m = m.marks
            except Marks.DoesNotExist:
                m = -1
            student_marks.append(m)

        if(ext_guide != -1):
            for r_id in rub_id:
                try:
                    m = marks.get(rubric_id=r_id, faculty=ext_guide[0])
                    m = m.marks
                except Marks.DoesNotExist:
                    m = -1
                student_marks.append(m)
        else:
            for r_id in rub_id:
                student_marks.append(-1)
        
        data.append(student_marks)

    return columns,data
