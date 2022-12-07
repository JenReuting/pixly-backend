\echo 'Delete and recreate pixly db?'
\prompt 'Return for yes or control-C to cancel > ' foo

DROP DATABASE pixly;
CREATE DATABASE pixly;
\connect pixly

\i pixly-schema.sql

\echo 'Delete and recreate pixly_test db?'
\prompt 'Return for yes or control-C to cancel > ' foo

DROP DATABASE pixly_test;
CREATE DATABASE pixly_test;
\connect pixly_test

\i pixly-schema.sql
