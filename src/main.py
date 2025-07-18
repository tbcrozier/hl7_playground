# generate_hl7.py

import os
from hl7apy.core import Message
from faker import Faker
from datetime import datetime

fake = Faker()

def build_fake_adt_message() -> Message:
    """Create and return one fake ADT^A01 message."""
    msg = Message("ADT_A01", version="2.5")
    now = datetime.now().strftime("%Y%m%d%H%M%S")
    msg.msh.msh_3 = "MySendingApp"
    msg.msh.msh_4 = "MyFacility"
    msg.msh.msh_5 = "TheirReceivingApp"
    msg.msh.msh_6 = "TheirFacility"
    msg.msh.msh_7 = now
    msg.msh.msh_9 = "ADT^A01"
    msg.msh.msh_10 = fake.uuid4()[:8]
    msg.msh.msh_11 = "P"
    msg.msh.msh_12 = msg.version

    pid = msg.pid
    pid.pid_3 = str(fake.random_number(digits=6))
    pid.pid_5 = f"{fake.last_name()}^{fake.first_name()}"
    pid.pid_7 = fake.date_of_birth(minimum_age=0, maximum_age=90).strftime("%Y%m%d")
    pid.pid_8 = fake.random_element(elements=["M","F","U"])
    pid.pid_11 = f"{fake.street_address()}^^{fake.city()}^{fake.state_abbr()}^{fake.zipcode()}"

    return msg

def save_hl7_message(msg: Message, filename: str,
                      output_dir: str = '/Users/ioa6870/repos/tbcrozier/hl7_playground/data/test_messages'):
    os.makedirs(output_dir, exist_ok=True)
    hl7_text = msg.to_er7()
    if not hl7_text.endswith('\r'):
        hl7_text += '\r'
    path = os.path.join(output_dir, filename)
    with open(path, 'wb') as f:
        f.write(hl7_text.encode('utf-8'))
    print(f"Wrote {path!r}")

if __name__ == "__main__":
    # Generate and save 100 fake ADT messages
    for i in range(1, 101):
        msg = build_fake_adt_message()
        save_hl7_message(msg, f'fake_adt_{i:03d}.hl7')
