import os
from django.core.management.base import CommandError
from django.core.management.commands.startapp import Command as StartAppCommand
from django.template import Context, Engine
from django.conf import settings

class Command(StartAppCommand):
    help = "Custom app creator with scenario files"
    
    def handle(self, *args, **options):
        print("CUSTOM COMMAND IS BEING EXECUTED!")  # Debug line
        super().handle(*args, **options)

        app_name = options['name']
        target = options.get('directory') or os.path.join(os.getcwd(), app_name)
        
        # Get the directory where THIS command file is located
        command_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Calculate template directory relative to the command location
        template_dir = os.path.join(command_dir, '..', '..', 'templates', 'app_template')
        template_dir = os.path.normpath(template_dir)  # Normalize the path
        
        print(f"Looking for templates in: {template_dir}")
        
        if not os.path.exists(template_dir):
            # Create a more helpful error message
            possible_locations = [
                os.path.join(os.getcwd(), 'templates', 'app_template'),
                os.path.join(settings.BASE_DIR, 'templates', 'app_template'),
                template_dir
            ]
            raise CommandError(
                "Template directory not found. Tried:\n" +
                "\n".join(f"- {path}" for path in possible_locations) +
                "\nPlease ensure the templates exist in one of these locations."
            )
        
        context = Context({
            'app_name': app_name,
            'app_name_title': app_name.title().replace('_', ''),
        }, autoescape=False)
        
        templates = [
            ('endpoints.py.template', 'endpoints.py'),
            ('scenarios.py.template', 'scenarios.py'),
        ]
        
        for template_name, output_name in templates:
            template_path = os.path.join(template_dir, template_name)
            output_path = os.path.join(target, output_name)
            
            if not os.path.exists(template_path):
                raise CommandError(f"Template file not found: {template_path}")
            
            with open(template_path, 'r') as template_file:
                content = template_file.read()
            
            engine = Engine()
            rendered = engine.from_string(content).render(context)
            
            with open(output_path, 'w') as output_file:
                output_file.write(rendered)
            
            print(f"Successfully created: {output_path}")