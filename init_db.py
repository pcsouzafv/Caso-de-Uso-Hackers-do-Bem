from app import app, db, User, Task, SystemLog

def init_db():
    with app.app_context():
        # Drop all tables
        db.drop_all()
        
        # Create all tables
        db.create_all()
        
        # Create admin user
        admin = User(username='admin', is_admin=True)
        admin.set_password('admin')
        db.session.add(admin)
        
        # Create test user
        user = User(username='user', is_admin=False)
        user.set_password('user')
        db.session.add(user)
        
        # Commit users
        db.session.commit()
        
        # Create some test tasks
        tasks = [
            Task(
                title='Welcome to Task Manager',
                description='This is your first task. Try marking it as complete!',
                user_id=2
            ),
            Task(
                title='Admin Task Example',
                description='This is an example task for the admin.',
                user_id=1
            )
        ]
        
        db.session.add_all(tasks)
        db.session.commit()
        
        print('Database initialized successfully!')

if __name__ == '__main__':
    init_db()
