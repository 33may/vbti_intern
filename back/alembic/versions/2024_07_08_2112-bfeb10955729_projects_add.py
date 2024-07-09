"""projects add

Revision ID: bfeb10955729
Revises: d7e6edb9463b
Create Date: 2024-07-08 21:12:23.423922

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import text

# revision identifiers, used by Alembic.
revision: str = 'bfeb10955729'
down_revision: Union[str, None] = 'd7e6edb9463b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.execute(text(
        """
        CREATE TABLE IF NOT EXISTS public.projects
        (
            id integer NOT NULL GENERATED ALWAYS AS IDENTITY (INCREMENT 1 START 1000 MINVALUE 1 MAXVALUE 2147483647 CACHE 1),
            name character varying(50) COLLATE pg_catalog."default" NOT NULL,
            description character varying(400) COLLATE pg_catalog."default",
            CONSTRAINT projects_pkey PRIMARY KEY (id)
        )
        TABLESPACE pg_default;
        
        ALTER TABLE IF EXISTS public.projects
            OWNER to admin;
        
        CREATE TABLE IF NOT EXISTS public.users_projects
        (
            user_id integer NOT NULL,
            project_id integer NOT NULL,
            CONSTRAINT users_projects_pkey PRIMARY KEY (user_id, project_id),
            CONSTRAINT fk_user
                FOREIGN KEY(user_id) 
                REFERENCES public.users(id) 
                ON DELETE CASCADE,
            CONSTRAINT fk_project
                FOREIGN KEY(project_id) 
                REFERENCES public.projects(id) 
                ON DELETE CASCADE
        )
        TABLESPACE pg_default;
        
        ALTER TABLE IF EXISTS public.users_projects
            OWNER to admin;
        
        -- Assuming the users table already exists and we are just adding a foreign key constraint
        ALTER TABLE public.users
            ADD CONSTRAINT fk_user_project
            FOREIGN KEY (project_id) REFERENCES public.projects (id) ON DELETE CASCADE;
        """
    ))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.execute(text(
        """
        CREATE TABLE IF NOT EXISTS public.projects
        (
            id integer NOT NULL GENERATED ALWAYS AS IDENTITY (INCREMENT 1 START 1000 MINVALUE 1 MAXVALUE 2147483647 CACHE 1),
            name character varying(50) COLLATE pg_catalog."default" NOT NULL,
            description character varying(400) COLLATE pg_catalog."default",
            CONSTRAINT projects_pkey PRIMARY KEY (id)
        )
        TABLESPACE pg_default;

        ALTER TABLE IF EXISTS public.projects
            OWNER to admin;

        CREATE TABLE IF NOT EXISTS public.users_projects
        (
            user_id integer NOT NULL,
            project_id integer NOT NULL,
            CONSTRAINT users_projects_pkey PRIMARY KEY (user_id, project_id),
            CONSTRAINT fk_user
                FOREIGN KEY(user_id) 
                REFERENCES public.users(id) 
                ON DELETE CASCADE,
            CONSTRAINT fk_project
                FOREIGN KEY(project_id) 
                REFERENCES public.projects(id) 
                ON DELETE CASCADE
        )
        TABLESPACE pg_default;

        ALTER TABLE IF EXISTS public.users_projects
            OWNER to admin;

        -- Assuming the users table already exists and we are just adding a foreign key constraint
        ALTER TABLE public.users
            ADD CONSTRAINT fk_user_project
            FOREIGN KEY (project_id) REFERENCES public.projects (id) ON DELETE CASCADE;
        """
    ))
    # ### end Alembic commands ###
