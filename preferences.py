import csv
import constants.type_ids

TYPE_IDS = constants.type_ids.TYPE_IDS

REGIONS = [
  'Domain',
  'Tash-Murkon',
  'Kador',
  'Kor-Azor',
  # 'Devoid',
  # 'Everyshore',
  # 'Genesis',
  # 'Providence',
  # 'Khanid',
  "The Bleak Lands",
  'Solitude',
]

ITEMS = [
  # Anything containing the word 'Datacores'
  # Anything containing the word 'Decryptors'
  # Anything containing the word 'Probe'
  # Anything containing the word 'Missle'

  # Ancient Salvage
  'Electromechanical Hull Sheeting',
  'Emergent Combat Analyzer',
  'Faraday Force Magnetometer',
  'Melted Nanoribbons',
  'Modified Fluid Router',
  'Scorched Microgravimeter',
  'Synthetic Aperture Ladar Receiver',

  # Salvage Materials
  "Armor Plates",
  "Artificial Neural Network",
  "Broken Drone Transceiver",
  "Burned Logic Circuit",
  "Capacitor Console",
  "Charred Micro Circuit",
  "Conductive Polymer",
  "Contaminated Lorentz Fluid",
  "Contaminated Nanite Compound",
  "Current Pump",
  "Damaged Artificial Neural Network",
  "Defective Current Pump",
  "Fried Interface Circuit",
  "Impetus Console",
  "Intact Armor Plates",
  "Interface Circuit",
  "Logic Circuit",
  "Lorentz Fluid",
  "Malfunctioning Shield Emitter",
  "Melted Capacitor Console",
  "Micro Circuit",
  "Nanite Compound",
  "Power Circuit",
  "Power Conduit",
  "Scorched Telemetry Processor",
  "Smashed Trigger Unit",
  "Tangled Power Conduit",
  "Telemetry Processor",
  "Trigger Unit",
  "Tripped Power Circuit",

  #
  "Antimatter Reactor Unit",
  "Ion Thruster",
  "Sleeper Nanite Cluster",

  # Minerals
  "Isogen",
  "Megacyte",
  "Mexallon",
  "Morphite",
  "Nocxium",
  "Pyerite",
  "Tritanium",
  "Zydrine",

  # Bounty Tags
  "Minmatar 1M Bounty Reimbursement Tag",
  "Caldari 10M Bounty Reimbursement Tag",
  "Amarr 1M Bounty Reimbursement Tag ",
  "Gallente 1M Bounty Reimbursement Tag",
  "Amarr 100K Bounty Reimbursement Tag ",
  "Caldari 100K Bounty Reimbursement Tag",
  "Gallente 100K Bounty Reimbursement Tag",
  "Minmatar 100K Bounty Reimbursement Tag",
  "Amarr 10K Bounty Reimbursement Tag ",
  "Caldari 10K Bounty Reimbursement Tag",
  "Gallente 10K Bounty Reimbursement Tag",
  "Minmatar 10K Bounty Reimbursement Tag",
  "Amarr 10M Bounty Reimbursement Tag ",
  "Gallente 10M Bounty Reimbursement Tag",
  "Minmatar 10M Bounty Reimbursement Tag",
  "Caldari 1M Bounty Reimbursement Tag",
]

ITEM_KEYWORDS = [
  "Datacore",
  "Decryptor",
  "Probe",
  "Missile",
  "Rocket",
  "Torpedo",
  "Implants",
  "Alpha",
  "Beta",
  "Gamma",
  "Delta",
  "Epsilon",
  "Skill",
  "Fullerite",
]

for item in TYPE_IDS:
  if any(keyword in item[1] for keyword in ITEM_KEYWORDS):
    ITEMS.append(item[1])
