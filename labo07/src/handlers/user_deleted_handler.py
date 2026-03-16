"""
Handler: User Deleted
SPDX-License-Identifier: LGPL-3.0-or-later
Auteurs : Gabriel C. Ullmann, Fabio Petrillo, 2025
"""

import os
from pathlib import Path
from handlers.base import EventHandler
from typing import Dict, Any

class UserDeletedHandler(EventHandler):
    """Handles UserDeleted events"""
    
    def __init__(self, output_dir: str = "output"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        super().__init__()
    
    def get_event_type(self) -> str:
        """Return the event type this handler processes"""
        return "UserDeleted"
    
    def handle(self, event_data: Dict[str, Any]) -> None:
        """Create an HTML email based on user deletion data"""
        user_id = event_data.get('id')
        name = event_data.get('name')
        email = event_data.get('email')
        deletion_datetime = event_data.get('datetime')
        user_type_id = event_data.get('user_type_id')

        current_file = Path(__file__)
        project_root = current_file.parent.parent

        with open(project_root / "templates" / "goodbye_client_template.html", 'r', encoding='utf-8') as file:
            html_content = file.read()
            html_content = html_content.replace("{{user_id}}", str(user_id))
            html_content = html_content.replace("{{name}}", name)
            html_content = html_content.replace("{{email}}", email)
            html_content = html_content.replace("{{deletion_date}}", deletion_datetime)

            # Personnaliser le message principal selon le type d'utilisateur
            base_message = "Nous supprimons votre compte à votre demande. Merci d'avoir été client de notre magasin. Si jamais vous voulez créer une nouvelle compte, n'hésitez pas à nous contacter."

            if user_type_id == 2:
                # Employé
                custom_message = "Nous supprimons ton compte employé. Merci pour ta contribution au sein de l'équipe du Magasin du Coin, et au plaisir de retravailler ensemble un jour."
                html_content = html_content.replace(base_message, custom_message)
            elif user_type_id == 3:
                # Directeur / directrice
                custom_message = "Nous supprimons ton compte de direction. Merci pour ton leadership au Magasin du Coin, et bonne continuation pour la suite."
                html_content = html_content.replace(base_message, custom_message)

        filename = os.path.join(self.output_dir, f"goodbye_{user_id}.html")
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html_content)

        self.logger.debug(f"Courriel HTML généré à {name} (ID: {user_id}), {filename}")