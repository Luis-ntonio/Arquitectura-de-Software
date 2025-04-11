-- optional.sql

-- Tabla de Abogados
CREATE TABLE Attorneys (
    attorney_id VARCHAR(255) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    phone VARCHAR(20),
    type VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de Clientes
CREATE TABLE Clients (
    client_id VARCHAR(255) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE,
    phone VARCHAR(20),
    address TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de Casos
CREATE TABLE Cases (
    case_id VARCHAR(255) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    status VARCHAR(50),
    description TEXT,
    attorney_id VARCHAR(255) REFERENCES Attorneys(attorney_id),
    client_id VARCHAR(255) REFERENCES Clients(client_id) NOT NULL,
    attachment_id VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de Archivos Adjuntos
CREATE TABLE Attachments (
    attachment_id VARCHAR(255) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    type VARCHAR(50),
    size INTEGER,
    url VARCHAR(512) NOT NULL,
    case_id VARCHAR(255) REFERENCES Cases(case_id) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de relación entre Abogados y Casos (only if needed for many-to-many)
CREATE TABLE AttorneyCases (
    attorney_case_id SERIAL PRIMARY KEY,
    attorney_id VARCHAR(255) REFERENCES Attorneys(attorney_id) NOT NULL,
    case_id VARCHAR(255) REFERENCES Cases(case_id) NOT NULL,
    UNIQUE (attorney_id, case_id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);