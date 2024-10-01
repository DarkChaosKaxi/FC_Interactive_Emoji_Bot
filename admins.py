from typing import Final
import os
from dotenv import load_dotenv

### Admins cache

load_dotenv()
admin_ids: Final[str] = [f'{os.getenv('KAXI_ID')}',f'{os.getenv('RIPLY_ID')}',f'{os.getenv('VOX_ID')}']
#admin_ids: Final[str] = os.getenv('ADMIN_IDS').split(',')

def check_admin(id: int) -> bool:
    for admin in admin_ids:
        print(f'Comparing {admin} and {id}.')
        if f'{id}' == admin:
            print('Admin identified!')
            return True
    print('User is not an Admin.')
    return True