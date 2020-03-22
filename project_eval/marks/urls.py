from django.urls import path
from .views import enterStudentMarksGuide,enterStudentMarksPanel,viewStudentMarks,updateStudentMarks,downloadPhaseMarks,downloadAllPhaseMarks

urlpatterns = [
    path('set_student_marks_guide/<str:usn>/<str:phase>/',enterStudentMarksGuide,name="enter_student_marks_guide"),
    path('set_student_marks_panel/<str:usn>/<str:phase>/',enterStudentMarksPanel,name="enter_student_marks_panel"),
    path('view_student_marks/<str:usn>/',viewStudentMarks,name="view_student_marks"),
    path('update_student_marks/<str:usn>/<str:phase>/',updateStudentMarks,name="update_student_marks"),
    path('download_phase_marks/<str:phase>/',downloadPhaseMarks,name="download_phase_marks"),
    path('download_all_phase_marks/',downloadAllPhaseMarks,name="download_all_phase_marks")
]