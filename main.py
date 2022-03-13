#!/usr/python3
from libs.dapodik import Dapodik
from libs.slims import Slims
import os
from dotenv import load_dotenv, find_dotenv


load_dotenv(find_dotenv())


def main():
    dapodik = Dapodik(
        os.getenv('DAPODIK_HOST'),
        os.getenv('DAPODIK_NPSN'), 
        os.getenv('DAPODIK_API_KEY')
    )
    
    slims = Slims(
        os.getenv('SLIMS_DATABASE_HOST'),
        os.getenv('SLIMS_DATABASE_PORT'),
        os.getenv('SLIMS_DATABASE_USERNAME'),
        os.getenv('SLIMS_DATABASE_PASSWORD'),
        os.getenv('SLIMS_DATABASE_DBNAME'),
    )
    
    studentStats = synchronizedStudents(dapodik, slims)
    teacherStats = synchronizedTeachers(dapodik, slims)
    
    print(studentStats)
    print("======================")
    print(teacherStats)
    

def synchronizedStudents(dapodik, slims):
    slims.deactivate(
        os.getenv('SLIMS_MEMBERSHIP_STUDENT_ID')
    )
    
    stats = {
        'total': 0,
        'updated': 0,
        'inserted': 0
    }
    
    for student in dapodik.getPesertaDidik():
        if student.memberId() == None:
            continue

        if slims.find(student.memberId(), os.getenv('SLIMS_MEMBERSHIP_STUDENT_ID')) != None:
            slims.update(student.toSlims())
            stats['updated'] = stats['updated'] + 1
        else:
            slims.insert(student.toSlims())
            stats['inserted'] = stats['inserted'] + 1
            
        stats['total'] = stats['total'] + 1
        
    slims.connection.commit()
            
    return stats
    
        

def synchronizedTeachers(dapodik, slims):
    slims.deactivate(
        os.getenv('SLIMS_MEMBERSHIP_TEACHER_ID')
    )
    
    stats = {
        'total': 0,
        'updated': 0,
        'inserted': 0
    }
    
    for teacher in dapodik.getGtk():
        if slims.find(teacher.memberId(), os.getenv('SLIMS_MEMBERSHIP_TEACHER_ID')) != None:
            slims.update(teacher.toSlims())
            stats['updated'] = stats['updated'] + 1
        else:
            slims.insert(teacher.toSlims())
            stats['inserted'] = stats['inserted'] + 1
            
        stats['total'] = stats['total'] + 1
        
    slims.connection.commit()
            
    return stats
    
    
if __name__ == '__main__':
    main()