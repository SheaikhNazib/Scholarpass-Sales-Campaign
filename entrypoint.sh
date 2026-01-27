#!/bin/bash

set -eu

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration from environment variables
DB_AUTO_MIGRATE="${DB_AUTO_MIGRATE:-true}"
ENVIRONMENT="${ENVIRONMENT:-development}"
SERVER_HOST="${SERVER_HOST:-0.0.0.0}"
SERVER_PORT="${SERVER_PORT:-8000}"
RELOAD_EXCLUDE="${RELOAD_EXCLUDE:-venv,.git,__pycache__,.pytest_cache,.venv}"

# Helper functions
log_info() {
    echo -e "${BLUE}ℹ $1${NC}"
}

log_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

log_error() {
    echo -e "${RED}✗ $1${NC}"
}

log_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

# Check if required commands exist
check_requirements() {
    log_info "Checking requirements..."
    
    if ! command -v alembic &> /dev/null; then
        log_error "Alembic is not installed"
        exit 1
    fi
    
    if ! command -v uvicorn &> /dev/null; then
        log_error "Uvicorn is not installed"
        exit 1
    fi
    
    log_success "All requirements met"
}

# Wait for database to be ready
wait_for_db() {
    log_info "Waiting for database to be ready..."
    
    max_attempts=30
    attempt=1
    
    while [ $attempt -le $max_attempts ]; do
        if python3 -c "
import os
from sqlalchemy import create_engine
try:
    engine = create_engine(os.getenv('DATABASE_URL', 'postgresql://scholarpass_user:scholarpass_password@db:5432/scholarpass_db'))
    with engine.connect() as conn:
        pass
    print('Database is ready')
except Exception as e:
    raise e
" 2>/dev/null; then
            log_success "Database is ready"
            return 0
        fi
        
        log_info "Database not ready yet... (attempt $attempt/$max_attempts)"
        sleep 1
        attempt=$((attempt + 1))
    done
    
    log_error "Database failed to become ready after $max_attempts attempts"
    exit 1
}

# Run database migrations
run_migrations() {
    log_info "Running Alembic migrations..."
    
    if [ "$DB_AUTO_MIGRATE" = "true" ]; then
        log_info "Database auto-migration is enabled"
        
        out="$(alembic upgrade head 2>&1)" || {
            code=$?
            echo "$out"
            
            # Check if it's a missing revision error
            echo "$out" | grep -q "Can't locate revision identified by" || {
                # Not a missing revision error, exit with error
                log_error "Alembic migration failed"
                exit $code
            }
            
            missing=$?
            
            if [ $missing -eq 0 ] && [ "$ENVIRONMENT" = "development" ]; then
                log_warning "Missing revision detected in development mode"
                log_info "DEV recovery: stamping to head, then upgrading..."
                
                alembic stamp head || {
                    log_error "Failed to stamp database"
                    exit 1
                }
                
                alembic upgrade head || {
                    log_error "Failed to upgrade database after stamping"
                    exit 1
                }
                
                log_success "Database recovered and upgraded"
            else
                log_error "Alembic migration failed"
                exit $code
            fi
        }
        
        log_success "Migrations completed successfully"
    else
        log_warning "Database auto-migration is disabled. Skipping migrations."
    fi
}

# Start the application
start_app() {
    log_info "Starting ScholarPASS Backend in $ENVIRONMENT mode..."
    
    if [ "$ENVIRONMENT" = "development" ]; then
        log_info "Starting with hot reload enabled"
        log_info "Server: http://$SERVER_HOST:$SERVER_PORT"
        log_info "API Docs: http://$SERVER_HOST:$SERVER_PORT/docs"
        
        # Build reload exclude arguments
        reload_args=""
        IFS=',' read -ra excludes <<< "$RELOAD_EXCLUDE"
        for exclude in "${excludes[@]}"; do
            reload_args="$reload_args --reload-exclude \"$exclude\""
        done
        
        eval "uvicorn src.main:app --host $SERVER_HOST --port $SERVER_PORT --reload $reload_args"
    else
        log_info "Starting in production mode"
        log_info "Server: http://$SERVER_HOST:$SERVER_PORT"
        
        uvicorn src.main:app --host "$SERVER_HOST" --port "$SERVER_PORT"
    fi
}

# Main execution
main() {
    log_info "=========================================="
    log_info "ScholarPASS Backend Startup"
    log_info "=========================================="
    log_info "Environment: $ENVIRONMENT"
    log_info "Server: $SERVER_HOST:$SERVER_PORT"
    log_info "Auto-migrate: $DB_AUTO_MIGRATE"
    log_info "=========================================="
    echo ""
    
    check_requirements
    wait_for_db
    run_migrations
    echo ""
    start_app
}

# Run main function
main "$@"
