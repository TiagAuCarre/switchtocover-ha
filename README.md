# SwitchToCover

[Version Française](#français)
[English Version](#english)

Home Assistant custom integration that turns an existing `switch` and a contact `binary_sensor` into a native `cover`.

The integration is designed for shutters, garage doors, gates, blinds, and other two-state openings controlled by a relay or switch.

## Features

- Fully configurable from the Home Assistant interface.
- One configuration entry creates one cover.
- Add as many garages, gates, blinds, or other openings as needed.
- Add new covers later with **Settings > Devices & services > Add integration**.
- Select source entities from entity pickers instead of typing IDs.
- Uses the contact sensor for the open/closed state.
- Uses `switch.turn_on` to open and `switch.turn_off` to close.
- Creates a separate Home Assistant device for every cover.

## Voice assistants

Because each opening is exposed as a native Home Assistant `cover`, it can be shared with compatible voice assistants such as Amazon Alexa and Google Home. After linking Home Assistant with the assistant of your choice, you can open and close a garage door or gate by voice, for example:

- "Alexa, open the garage."
- "Hey Google, close the gate."

The assistant integration must be configured separately in Home Assistant. The exact availability and commands depend on the assistant, your Home Assistant setup, and the entities you choose to expose.

## Installation

1. Copy the `switch_to_cover` folder into the `custom_components` folder of your Home Assistant configuration directory.
2. Restart Home Assistant.
3. Open **Settings > Devices & services**.
4. Select **Add integration** and search for **SwitchToCover**.
5. Configure one opening at a time.

The folder name must remain `switch_to_cover` because it matches the integration domain. The integration shown in Home Assistant is named **SwitchToCover**.

## Configuration

For each opening, choose:

- A name, such as `Garage`, `Portail`, `Garage 2`, or `Store salon`.
- A type: garage, gate, or other.
- The switch that controls the motor or relay.
- The contact binary sensor that reports the opening state.

For the original example:

| Cover | Switch | Contact sensor |
| --- | --- | --- |
| Garage | `switch.exterieur_garage` | `binary_sensor.garage_contact` |
| Portail | `switch.exterieur_portail` | `binary_sensor.portail_contact` |

To add another opening, add **SwitchToCover** again and choose the new pair of entities. Existing entries remain untouched.

## State convention

The contact sensor is interpreted as follows:

- `off`: closed
- `on`: open

If your sensor uses the opposite convention, invert the sensor in Home Assistant or create a template binary sensor with the expected convention.

## Entities and attributes

Each configuration entry creates one `cover` entity. The entity exposes these attributes to help with automations and troubleshooting:

- `switch_entity`: the linked switch entity ID.
- `contact_entity`: the linked contact sensor entity ID.

## Limitations

The source switch is treated as a command relay. The contact sensor is the source of truth for the final open or closed position. Intermediate opening and closing states are inferred from both entities and may be limited by the speed of the contact sensor.

## Français

SwitchToCover est une intégration personnalisée pour Home Assistant qui transforme un `switch` existant et un `binary_sensor` de contact en un vrai `cover`.

Elle convient aux portes de garage, portails, volets, stores et autres ouvrants commandés par un relais ou un interrupteur.

### Fonctions

- Ajout entièrement réalisé depuis l'interface de Home Assistant.
- Une configuration crée un ouvrant.
- Nombre illimité de garages, portails, volets ou autres ouvrants.
- Ajout de nouveaux ouvrants plus tard depuis **Paramètres > Appareils et services > Ajouter une intégration**.
- Sélection des entités dans des listes, sans devoir saisir les identifiants à la main.
- Le capteur de contact indique si l'ouvrant est ouvert ou fermé.
- `switch.turn_on` ouvre et `switch.turn_off` ferme.
- Chaque ouvrant est créé comme un appareil Home Assistant séparé.

### Assistants vocaux

Comme chaque ouvrant est exposé comme un vrai `cover` Home Assistant, il peut être partagé avec des assistants vocaux compatibles comme Amazon Alexa et Google Home. Après avoir relié Home Assistant à l'assistant de ton choix, tu peux ouvrir ou fermer ton garage ou ton portail à la voix, par exemple :

- « Alexa, ouvre le garage. »
- « Hey Google, ferme le portail. »

L'intégration avec Alexa ou Google Home doit être configurée séparément dans Home Assistant. Les commandes disponibles dépendent de l'assistant utilisé, de ta configuration Home Assistant et des entités que tu choisis d'exposer.

### Installation

1. Copie le dossier `switch_to_cover` dans le dossier `custom_components` de ta configuration Home Assistant.
2. Redémarre Home Assistant.
3. Va dans **Paramètres > Appareils et services**.
4. Clique sur **Ajouter une intégration** et cherche **SwitchToCover**.
5. Configure un ouvrant à la fois.

Le dossier doit rester nommé `switch_to_cover`. Le nom visible dans Home Assistant est **SwitchToCover**.

### Configuration de tes entités

Pour ton installation actuelle, ajoute deux configurations :

| Ouvrant | Interrupteur | Capteur de contact |
| --- | --- | --- |
| Garage | `switch.exterieur_garage` | `binary_sensor.garage_contact` |
| Portail | `switch.exterieur_portail` | `binary_sensor.portail_contact` |

Pour ajouter un deuxième garage ou un deuxième portail, relance simplement **Ajouter une intégration > SwitchToCover** et sélectionne les nouvelles entités.

### Convention du capteur

- `off` signifie fermé.
- `on` signifie ouvert.

Si ton capteur fonctionne à l'inverse, inverse-le dans Home Assistant ou crée un capteur binaire template avec cette convention.

## License

MIT License. See `LICENSE` if one is included by the project owner.
