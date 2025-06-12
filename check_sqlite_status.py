#!/usr/bin/env python
"""
SQLite Database Status Checker for cPanel Deployment
Run this script to verify your SQLite database setup.
"""

import os
import sys
import django
from pathlib import Path

# Add the current directory to Python path
current_dir = Path(__file__).resolve().parent
sys.path.insert(0, str(current_dir))

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fc_backend.settings')

try:
    django.setup()
    from django.conf import settings
    from django.db import connection
    from django.apps import apps
    
    print("🚀 SQLite Database Status Check")
    print("=" * 40)
    
    # Database configuration
    db_config = settings.DATABASES['default']
    print(f"✅ Database Engine: {db_config['ENGINE']}")
    print(f"📁 Database File: {db_config['NAME']}")
    
    # Check if database file exists
    db_path = Path(db_config['NAME'])
    if db_path.exists():
        size_mb = db_path.stat().st_size / (1024 * 1024)
        print(f"✅ Database file exists ({size_mb:.2f} MB)")
        
        # Test connection
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT COUNT(*) FROM sqlite_master WHERE type='table'")
                table_count = cursor.fetchone()[0]
                print(f"📊 Database tables: {table_count}")
                
                # Check for Django tables
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name LIKE 'django_%'")
                django_tables = cursor.fetchall()
                print(f"🔧 Django system tables: {len(django_tables)}")
                
                # Check for user tables
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'django_%' AND name != 'sqlite_sequence'")
                user_tables = cursor.fetchall()
                print(f"👤 Application tables: {len(user_tables)}")
                
                if user_tables:
                    print("📋 Application tables:")
                    for table in user_tables:
                        print(f"   - {table[0]}")
                
        except Exception as e:
            print(f"❌ Database connection error: {e}")
            
    else:
        print("⚠️  Database file doesn't exist yet")
        print("💡 Run 'python manage.py migrate' to create it")
    
    # Check for pending migrations
    try:
        from django.core.management import execute_from_command_line
        from django.core.management.commands.showmigrations import Command as ShowMigrationsCommand
        from django.db.migrations.executor import MigrationExecutor
        
        executor = MigrationExecutor(connection)
        plan = executor.migration_plan(executor.loader.graph.leaf_nodes())
        
        if plan:
            print(f"⚠️  Pending migrations: {len(plan)}")
            print("💡 Run 'python manage.py migrate' to apply them")
        else:
            print("✅ No pending migrations")
            
    except Exception as e:
        print(f"⚠️  Migration check failed: {e}")
    
    # Environment check
    print("\n🔧 Environment Configuration")
    print("=" * 40)
    print(f"DEBUG: {settings.DEBUG}")
    print(f"ALLOWED_HOSTS: {settings.ALLOWED_HOSTS}")
    print(f"STATIC_ROOT: {settings.STATIC_ROOT}")
    print(f"STATIC_URL: {settings.STATIC_URL}")
    
    # Check static files
    static_path = Path(settings.STATIC_ROOT) if settings.STATIC_ROOT else None
    if static_path and static_path.exists():
        print(f"✅ Static files directory exists")
    else:
        print("⚠️  Static files not collected")
        print("💡 Run 'python manage.py collectstatic' to create them")
    
    print("\n🎉 SQLite Status Check Complete!")
    
except ImportError as e:
    print(f"❌ Django import error: {e}")
    print("💡 Make sure you're in the correct directory and Django is installed")
except Exception as e:
    print(f"❌ Unexpected error: {e}")
    import traceback
    traceback.print_exc()

print("\n📚 Quick Commands:")
print("   python manage.py migrate          # Create/update database")
print("   python manage.py collectstatic   # Collect static files")
print("   python manage.py createsuperuser # Create admin user")
print("   python manage.py runserver       # Test locally")
