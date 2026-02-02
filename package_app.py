import shutil
import os
import datetime

def zip_project():
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    zip_filename = f"medtrack_production_{timestamp}"
    
    # Define source directory (current dir)
    source_dir = os.getcwd()
    
    # Create a temporary folder to organize what goes into the zip
    base_dir = os.path.join(source_dir, zip_filename)
    if not os.path.exists(base_dir):
        os.makedirs(base_dir)
        
    print(f"[Packaging MedTrack for Migration...]")
    print(f"Source: {source_dir}")
    
    # Files to include
    include_files = [
        'app.py', 'database.py', 'database_dynamo.py', 'server.py', 'ml_engine.py', 
        'signal_diagnostic.py', 'image_diagnostic.py', 'aws_setup.py', 'reference_aws_setup.py',
        'sns_service.py',
        'requirements.txt', 'requirements-lite.txt', 
        'Dockerfile', 'docker-compose.yml', 'deployment.md',
        'Procfile', '.gitignore'
    ]
    
    include_dirs = ['templates', 'static', 'medtrack'] # medtrack for uploads if needed
    
    # Copy files
    for f in include_files:
        if os.path.exists(f):
            shutil.copy2(f, base_dir)
            
    # Copy directories
    for d in include_dirs:
        if os.path.exists(d):
            # Ignore __pycache__ inside directories
            shutil.copytree(d, os.path.join(base_dir, d), 
                          ignore=shutil.ignore_patterns('__pycache__', '*.pyc', '.git'))

    # Create Zip
    shutil.make_archive(zip_filename, 'zip', base_dir)
    
    # Cleanup temp folder
    shutil.rmtree(base_dir)
    
    print(f"[Success] Created deployment package: {zip_filename}.zip")
    print(f"Upload this zip file to your commercial hosting provider context.")

if __name__ == "__main__":
    zip_project()
