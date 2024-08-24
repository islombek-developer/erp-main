from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render,get_object_or_404,redirect
from  users.permissionmixin import TeacherRequiredMixin
from  django.views import  View
from  users.models import Teacher,Student,User
from  students.models import Lesson,Team,Homework,Davomat
from users.forms import ProfileForm,ResetPasswordForm
from .forms import CreateLessonForm,DavomatForm
from django.urls import reverse


class TeacherView(TeacherRequiredMixin,View):
    def get(self,request):
        return render(request,'teachers/dashboard.html')

class TeacherTimesView(TeacherRequiredMixin,View):
    def get(self,request):
        teacher = get_object_or_404(Teacher,user=request.user)
        teams = teacher.teacher.all()
        return render(request,'teachers/guruhlarim.html',{"teams":teams})

class TeacherGroup(TeacherRequiredMixin,View):
    def get(self,request,team_id):
        team = get_object_or_404(Team,id=team_id)
        lessons = team.lesson.all()
        return render(request,'teachers/guruh.html',{'team':team,'lessons':lessons})

class TeacherHomeworks(TeacherRequiredMixin,View):
    def get(self,request,team_id):
        team = get_object_or_404(Team,id=team_id)
        lessons = team.homeworks.all()
        return render(request,'teachers/guruh.html',{'team':team,'lessons':lessons})

class TeacherStudentsView(TeacherRequiredMixin,View):
    def get(self,request,team_id):
        team = get_object_or_404(Team,id=team_id)
        student = team.students.all()
        return render(request,'teachers/student.html',{'team':team,'student':student})

class ProfileView(LoginRequiredMixin,View):
    def get(self,request):
        user = request.user
        return render(request,'teachers/profil.html',context={"user":user})

class TeacherHomevorkStudent(TeacherRequiredMixin,View):
    def get(self,request,team_id):
        team = get_object_or_404(Team,id=team_id)
        lessons = team.lesson.all()
        return render(request,'teachers/guruh.html',{'team':team,'lessons':lessons})

class EditProfileView(LoginRequiredMixin, View):
    def get(self, request, id):
        user = get_object_or_404(User, id=id)
        form = ProfileForm(instance=user)
        return render(request, 'teachers/edit.html', {'form': form})

    def post(self, request, id):
        user = get_object_or_404(User, id=id)
        form = ProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('teachers:profil')  
        return render(request, 'teachers/edit.html', {'form': form})

class ResetPasswordView(LoginRequiredMixin,View):
    def get(self, request):
        form = ResetPasswordForm()
        return render(request, 'teachers/reset_password.html', {'form':form})

    def post(self, request):
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            new_password = form.cleaned_data['new_password']
            user = request.user
            user.set_password(new_password)
            user.save()
            return redirect('/')
        form = ResetPasswordForm()
        return render(request, 'teachers/reset_password.html', {'form':form})


class TeacherCreateLessonView(TeacherRequiredMixin, View):
    def get(self, request, team_id):
        form = CreateLessonForm()
        return render(request, 'teachers/create_lesson.html', {'form': form})

    def post(self, request, team_id):
        team = get_object_or_404(Team, id=team_id)
        form = CreateLessonForm(request.POST, request.FILES)
        if form.is_valid():
            lesson = Lesson(
                team=team,
                title=form.cleaned_data['title'],
                lesson_file=form.cleaned_data['lesson_file'],
            )
            lesson.save()
            url = reverse('teachers:homeworks', args=[team_id])
            return redirect(url)
        return render(request, 'teachers/create_lesson.html', {'form': form})


class TeacherStudentLeson(TeacherRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        lesson_id = kwargs.get('id')  
        lesson = get_object_or_404(Lesson, id=lesson_id)
        homeworks = Homework.objects.filter(lesson=lesson).select_related('student', 'team')
        return render(request, 'teachers/students.html', {'homeworks': homeworks, 'lesson': lesson})

class TeacherHomeworkListView(TeacherRequiredMixin, View):
    def get(self, request):
        lessons = Lesson.objects.filter(team__teacher=request.user.teacher)
        homeworks = Homework.objects.filter(lesson__in=lessons).select_related('student__user', 'lesson')
        return render(request, 'teachers/homework_list.html', {'homeworks': homeworks})




class DavomatListView(View):
    def get(self, request, id):
        team = get_object_or_404(Team, id=id)
        students = team.students.all()
        davomat_records = Davomat.objects.filter(team=team)
        
        # Create a dictionary to easily access attendance status per student
        student_attendance = {
            student.id: {
                'name': student.user.first_name,
                'status': next((d.status for d in davomat_records if d.student == student), False)
            }
            for student in students
        }
        
        form = DavomatForm()
        return render(request, 'teachers/davomat_list.html', {
            'students': students,
            'team': team,
            'student_attendance': student_attendance,
            'form': form
        })

    def post(self, request, id):
        team = get_object_or_404(Team, id=id)
        students = team.students.all()

        # Process attendance for each student
        for student in students:
            status = request.POST.get(f'status_{student.id}', 'off') == 'on'
            Davomat.objects.update_or_create(
                team=team,
                student=student,
                defaults={'status': status}
            )

        messages.success(request, "Attendance saved successfully.")
        return redirect('teachers:student')   