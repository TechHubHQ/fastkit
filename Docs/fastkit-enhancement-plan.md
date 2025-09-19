# FastKit Enhancement Plan: Optional Feature Commands

## 🎯 Overview

This plan outlines the implementation of optional feature commands that allow users to add specific core and middleware components to their FastKit projects on-demand.

## 📋 Command Structure

### Base Command Pattern
```bash
fastkit add-feature <category> <feature_name> [options]
```

### Categories
- **core** - Core application features
- **middleware** - HTTP middleware components
- **utils** - Utility functions and helpers

## 🚀 Proposed Commands

### 1. Core Features

#### Events System
```bash
fastkit add-feature core events
```
**What it adds:**
- `app/core/events.py` - Startup/shutdown event handlers
- Database connection initialization
- Cache connection setup
- Background task initialization

#### Email Service
```bash
fastkit add-feature core email [--provider smtp|sendgrid|ses]
```
**What it adds:**
- `app/core/email.py` - Email service with templates
- Email configuration in settings
- Dependencies for chosen provider

#### File Handling
```bash
fastkit add-feature core files [--storage local|s3|gcs]
```
**What it adds:**
- `app/core/files.py` - File upload/download utilities
- Storage configuration
- File validation and processing

#### Validation System
```bash
fastkit add-feature core validators
```
**What it adds:**
- `app/core/validators.py` - Custom Pydantic validators
- Common validation patterns (email, phone, etc.)

#### Constants & Enums
```bash
fastkit add-feature core constants
fastkit add-feature core enums
```
**What it adds:**
- `app/core/constants.py` - Application constants
- `app/core/enums.py` - Application enums

### 2. Middleware Features

#### Rate Limiting
```bash
fastkit add-feature middleware rate-limiting [--backend redis|memory]
```
**What it adds:**
- `app/shared/middleware/rate_limit.py` - Rate limiting middleware
- Configuration for rate limits
- Backend-specific dependencies

#### Request ID Tracking
```bash
fastkit add-feature middleware request-id
```
**What it adds:**
- `app/shared/middleware/request_id.py` - Request ID middleware
- Correlation ID headers
- Request tracing utilities

#### Security Headers
```bash
fastkit add-feature middleware security-headers
```
**What it adds:**
- `app/shared/middleware/security_headers.py` - Security headers middleware
- HSTS, CSP, X-Frame-Options, etc.
- Configurable security policies

#### Response Compression
```bash
fastkit add-feature middleware compression
```
**What it adds:**
- `app/shared/middleware/compression.py` - Gzip compression middleware
- Configurable compression settings

#### Authentication Middleware
```bash
fastkit add-feature middleware auth-middleware [--type jwt|oauth]
```
**What it adds:**
- `app/shared/middleware/auth.py` - Authentication middleware
- Token validation
- User context injection

#### Database Session Management
```bash
fastkit add-feature middleware database-session
```
**What it adds:**
- `app/shared/middleware/database.py` - Auto session management
- Transaction handling
- Connection pooling optimization

### 3. Utility Features

#### Enhanced Logging
```bash
fastkit add-feature utils logging [--format json|text] [--level debug|info|warning|error]
```
**What it adds:**
- `app/shared/utils/logger.py` - Structured logging configuration
- Log formatters and handlers
- Environment-specific logging

#### Helper Functions
```bash
fastkit add-feature utils helpers
```
**What it adds:**
- `app/shared/utils/helpers.py` - Common utility functions
- String manipulation, data conversion, etc.

#### Date/Time Utilities
```bash
fastkit add-feature utils datetime
```
**What it adds:**
- `app/shared/utils/datetime.py` - Date/time utilities
- Timezone handling, formatting, parsing

#### Encryption Utilities
```bash
fastkit add-feature utils encryption
```
**What it adds:**
- `app/shared/utils/encryption.py` - Encryption/hashing utilities
- Password hashing, token generation, etc.

#### Validation Utilities
```bash
fastkit add-feature utils validation
```
**What it adds:**
- `app/shared/utils/validation.py` - Validation helper functions
- Email, phone, URL validators

## 🏗️ Implementation Architecture

### 1. Command Structure

```
fastkit/
├── cli/
│   └── commands/
│       └── add_feature.py          # Main feature command
├── generators/
│   ├── feature_generator.py        # Feature generation logic
│   └── templates/
│       └── features/               # Feature templates
│           ├── core/
│           │   ├── events.py.jinja
│           │   ├── email.py.jinja
│           │   ├── files.py.jinja
│           │   └── ...
│           ├── middleware/
│           │   ├── rate_limit.py.jinja
│           │   ├── request_id.py.jinja
│           │   └── ...
│           └── utils/
│               ├── logging.py.jinja
│               ├── helpers.py.jinja
│               └── ...
```

### 2. Feature Configuration

Each feature will have a configuration file defining:
- Dependencies to add
- Files to create
- Configuration updates needed
- Integration points

```yaml
# features/middleware/rate-limiting.yaml
name: rate-limiting
category: middleware
description: "API rate limiting and throttling"
dependencies:
  redis: ["redis>=4.0.0"]
  memory: ["cachetools>=5.0.0"]
files:
  - template: "middleware/rate_limit.py.jinja"
    destination: "app/shared/middleware/rate_limit.py"
config_updates:
  - file: "app/core/config.py"
    section: "rate_limiting"
integration:
  - file: "app/main.py"
    middleware: "RateLimitMiddleware"
```

### 3. Dependency Management Integration

Features will integrate with the existing dependency management system:
- Automatically add required packages to `pyproject.toml`
- Handle version conflicts
- Support optional dependencies based on provider choice

### 4. Template System

Each feature template will be context-aware:
- Detect existing project configuration
- Adapt to chosen database/cache/auth providers
- Maintain consistency with project structure

## 🔧 Implementation Steps

### Phase 1: Core Infrastructure
1. Create `add-feature` command structure
2. Implement feature generator with template system
3. Create feature configuration system
4. Integrate with dependency manager

### Phase 2: Essential Features
1. **Rate Limiting** - Most requested feature
2. **Request ID** - Essential for debugging
3. **Security Headers** - Important for production
4. **Enhanced Logging** - Critical for monitoring

### Phase 3: Advanced Features
1. **Events System** - For complex applications
2. **Email Service** - Common requirement
3. **File Handling** - For file upload scenarios
4. **Authentication Middleware** - For protected APIs

### Phase 4: Utility Features
1. **Helper Functions** - Developer productivity
2. **Validation Utilities** - Data integrity
3. **Encryption Utilities** - Security features
4. **DateTime Utilities** - Common operations

## 📝 Command Examples

### Basic Usage
```bash
# Add rate limiting with Redis backend
fastkit add-feature middleware rate-limiting --backend redis

# Add request ID tracking
fastkit add-feature middleware request-id

# Add security headers
fastkit add-feature middleware security-headers

# Add enhanced logging with JSON format
fastkit add-feature utils logging --format json --level info
```

### Advanced Usage
```bash
# Add email service with SendGrid
fastkit add-feature core email --provider sendgrid

# Add file handling with S3 storage
fastkit add-feature core files --storage s3

# Add authentication middleware for JWT
fastkit add-feature middleware auth-middleware --type jwt
```

### List Available Features
```bash
# List all available features
fastkit list-features

# List features by category
fastkit list-features --category middleware
fastkit list-features --category core
fastkit list-features --category utils
```

### Feature Information
```bash
# Get detailed information about a feature
fastkit feature-info middleware rate-limiting
fastkit feature-info core email
```

## 🎨 User Experience

### Interactive Mode
```bash
fastkit add-feature
# Prompts user to select:
# 1. Category (core/middleware/utils)
# 2. Feature from available list
# 3. Configuration options
# 4. Confirmation before installation
```

### Help System
```bash
fastkit add-feature --help
# Shows all available categories and features

fastkit add-feature middleware --help
# Shows all middleware features with descriptions

fastkit add-feature middleware rate-limiting --help
# Shows specific options for rate limiting
```

## 🔍 Benefits

### For Users
- **Modular**: Add only needed features
- **Discoverable**: Easy to find and understand features
- **Consistent**: All features follow same patterns
- **Production-Ready**: Features are tested and optimized

### For Developers
- **Extensible**: Easy to add new features
- **Maintainable**: Clear separation of concerns
- **Testable**: Each feature can be tested independently
- **Documented**: Self-documenting through help system

## 🚦 Success Metrics

- **Adoption Rate**: How many users use add-feature commands
- **Feature Usage**: Which features are most popular
- **User Feedback**: Satisfaction with feature quality
- **Contribution**: Community contributions of new features

## 🔮 Future Enhancements

### Advanced Features
- **Feature Profiles**: Predefined feature bundles (e.g., "production-ready", "development", "microservices")
- **Feature Dependencies**: Automatic installation of dependent features
- **Feature Updates**: Update existing features to newer versions
- **Custom Features**: User-defined feature templates

### Integration
- **IDE Integration**: VS Code extension for feature management
- **CI/CD Integration**: Automated feature installation in pipelines
- **Monitoring**: Built-in monitoring for installed features

## 📋 Implementation Checklist

### Core Infrastructure
- [ ] Create `add-feature` command
- [ ] Implement feature generator
- [ ] Create template system
- [ ] Integrate dependency management
- [ ] Add feature configuration system

### Essential Features
- [ ] Rate limiting middleware
- [ ] Request ID middleware
- [ ] Security headers middleware
- [ ] Enhanced logging utilities

### Documentation
- [ ] Feature documentation
- [ ] Usage examples
- [ ] Best practices guide
- [ ] Migration guide

### Testing
- [ ] Unit tests for feature generator
- [ ] Integration tests for features
- [ ] End-to-end testing
- [ ] Performance testing

This plan provides a comprehensive approach to making FastKit more modular and user-friendly while maintaining the high quality and production-readiness that users expect.