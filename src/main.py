import os
from hl7apy.core import Message
from faker import Faker
from datetime import datetime

def save_hl7_message(msg: Message, filename: str,
                      output_dir: str = '/Users/ioa6870/repos/tbcrozier/hl7_playground/data/test_messages'):
    # 1. ensure the output dir exists
    os.makedirs(output_dir, exist_ok=True)

    # 2. serialize using the default \r terminators
    hl7_text = msg.to_er7()
    # add a trailing \r if you want the file to end in a segment terminator
    if not hl7_text.endswith('\r'):
        hl7_text += '\r'

    # 3. write as UTF-8 bytes so we don’t accidentally mangle the \r
    path = os.path.join(output_dir, filename)
    with open(path, 'wb') as f:
        f.write(hl7_text.encode('utf-8'))

    print(f"Wrote HL7 message to {path!r}")

# --- usage example ---
fake = Faker()
msg = Message("ADT_A01", version="2.5")

# populate MSH & PID as before…
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

# now save it
save_hl7_message(msg, 'adt_a01_001.hl7')