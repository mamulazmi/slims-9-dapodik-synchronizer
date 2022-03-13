#!/usr/python3
from libs.dapodik import Dapodik
from libs.slims import Slims
from schedule import every, repeat, run_pending
import time
import os
from dotenv import load_dotenv, find_dotenv
from tabulate import tabulate

load_dotenv(find_dotenv())

@repeat(every().day.at("01:00"))
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
    
    
    table = [
        ['Synchronized Students', studentStats['inserted'], studentStats['updated'], studentStats['total']],
        ['Synchronized Teachers', teacherStats['inserted'], teacherStats['updated'], teacherStats['total']]
    ]
    
    
    print(
        tabulate(table, 
            tablefmt='fancy_grid',
            headers=['Type', 'Inserted', 'Updated', 'Total']
        )
    )
    

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
        
    slims.commit()
            
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
        if teacher.memberId() == None:
            continue
        
        if slims.find(teacher.memberId(), os.getenv('SLIMS_MEMBERSHIP_TEACHER_ID')) != None:
            slims.update(teacher.toSlims())
            stats['updated'] = stats['updated'] + 1
        else:
            slims.insert(teacher.toSlims())
            stats['inserted'] = stats['inserted'] + 1
            
        stats['total'] = stats['total'] + 1
        
    slims.commit()
            
    return stats
    
    
if __name__ == '__main__':
    main()
    while True:
        run_pending()
        time.sleep(1)