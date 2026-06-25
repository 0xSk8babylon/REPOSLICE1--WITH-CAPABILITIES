# 1Password reference template for production Gate 2 preapproved runtime delivery.
# This file contains no resolved secrets.
#
# DATABASE_URL intentionally maps to DATABASE_PUBLIC_URL so local Alembic can
# reach the Railway production Postgres service during Gate 2.
APP_ENV=production
DEBUG=false
DATABASE_URL="op://TwinEnergy/j3qbtqgq3ywnrem3hxxcx2ngle/DATABASE_PUBLIC_URL"
DATABASE_CREATE_ALL_ON_STARTUP=false
DATABASE_SEED_DEMO_DATA_ON_STARTUP=false
