# Implementation Plan Phase 2: Missing Features

## Overview
This plan addresses the missing features identified in the Game AI Assistant Analysis Report, prioritizing database integration, history management, and configuration systems.

## Phase 2.1: Database Integration (Priority 1)

### 1. Database Models
Create `server/src/models/interaction.py`:
```python
class Interaction(Base):
    __tablename__ = "interactions"
    
    id: int (Primary Key)
    timestamp: datetime
    screenshot_path: str (optional)
    screenshot_base64: text (store inline)
    question_text: str
    question_audio_path: str (optional)
    response_text: str
    response_audio_path: str (optional)
    llm_provider: str (claude/openai)
    system_prompt: str
    processing_time_ms: int
    user_rating: int (optional, 1-5)
```

### 2. Database Service
Create `server/src/services/database_service.py`:
- Initialize SQLite connection
- CRUD operations for interactions
- Search functionality
- Export/import capabilities
- Automatic cleanup of old records

### 3. History Endpoints
Create `server/src/api/endpoints/history.py`:
- `GET /api/v1/history` - List interactions with pagination
- `GET /api/v1/history/{id}` - Get specific interaction
- `DELETE /api/v1/history/{id}` - Delete interaction
- `POST /api/v1/history/search` - Search interactions
- `GET /api/v1/history/export` - Export as JSON/CSV

### 4. Client Integration
Update `client/src/main.py`:
- Store interaction IDs after each request
- Add hotkey for history (Ctrl+Shift+H)
- Show last 5 interactions in overlay

## Phase 2.2: Enhanced UI System (Priority 2)

### 1. History Panel
Update `client/src/ui/overlay.py`:
```python
class HistoryPanel:
    - Scrollable list of past interactions
    - Click to view full response
    - Copy button for each entry
    - Delete button
    - Search box
    - Export button
```

### 2. Settings Dialog
Create `client/src/ui/settings_dialog.py`:
```python
class SettingsDialog:
    - API Keys configuration (secure input)
    - Hotkey customization
    - Default LLM provider selection
    - Audio settings (input device, volume)
    - UI preferences (opacity, position, size)
    - Game profiles management
```

### 3. Visual Feedback System
Create `client/src/ui/recording_indicator.py`:
- Red border overlay during recording
- Pulsing animation
- Countdown timer for auto-stop
- Audio level indicator

## Phase 2.3: Configuration Management (Priority 3)

### 1. Settings Model
Create `shared/models/settings.py`:
```python
@dataclass
class UserSettings:
    # API Configuration
    anthropic_api_key: str (encrypted)
    openai_api_key: str (encrypted)
    preferred_llm: str = "claude"
    
    # Hotkeys
    hotkeys: Dict[str, str] = {
        "claude_analysis": "ctrl+shift+c",
        "openai_analysis": "ctrl+shift+v",
        "history": "ctrl+shift+h",
        "settings": "ctrl+shift+comma"
    }
    
    # Audio Settings
    input_device: str = "default"
    silence_threshold: float = 0.01
    silence_duration: float = 2.0
    tts_voice: str = "default"
    
    # UI Settings
    overlay_opacity: float = 0.9
    overlay_position: Tuple[int, int] = (100, 100)
    overlay_size: Tuple[int, int] = (400, 300)
    theme: str = "sci-fi"
```

### 2. Configuration Service
Create `client/src/services/config_service.py`:
- Load/save settings from `%APPDATA%/GameAI/settings.json`
- Encrypt sensitive data (API keys)
- Validate settings
- Import/export functionality
- Reset to defaults

### 3. Server Configuration
Update `server/src/core/config.py`:
- Centralized configuration management
- Environment variable overrides
- Configuration validation
- Feature flags

## Phase 2.4: Memory System Foundation (Priority 4)

### 1. Basic Context Storage
Create `server/src/services/memory_service.py`:
```python
class MemoryService:
    def store_interaction(self, interaction: Interaction):
        # Store in database with embeddings placeholder
        
    def get_session_context(self, session_id: str) -> List[Interaction]:
        # Get last N interactions from session
        
    def get_game_context(self, game_name: str) -> List[Interaction]:
        # Get relevant interactions for specific game
```

### 2. Session Management
- Add session_id to all interactions
- Group interactions by gaming session
- Automatic session detection (time-based)
- Session summary generation

### 3. Context Injection
Update LLM services to include context:
- Last 3-5 interactions as context
- Game-specific knowledge
- User preferences

## Phase 2.5: Testing & Quality (Priority 5)

### 1. Unit Tests
Create comprehensive tests for:
- Database operations
- History management
- Configuration handling
- UI components
- Service integrations

### 2. Integration Tests
- End-to-end workflow tests
- API endpoint tests with mocked LLMs
- Database transaction tests
- Configuration persistence tests

### 3. Mock Infrastructure
Implement proper mocks for:
- LLM services (OpenAI, Claude)
- Audio recording
- Screenshot capture
- TTS generation

## Implementation Timeline

### Week 1
- [ ] Database models and migrations
- [ ] Database service implementation
- [ ] History API endpoints
- [ ] Basic history storage

### Week 2
- [ ] History panel UI
- [ ] Settings dialog UI
- [ ] Configuration service
- [ ] Settings persistence

### Week 3
- [ ] Visual feedback system
- [ ] Session management
- [ ] Context injection
- [ ] Memory service foundation

### Week 4
- [ ] Comprehensive testing
- [ ] Documentation updates
- [ ] Performance optimization
- [ ] Bug fixes and polish

## Success Criteria

1. **Database Integration**
   - All interactions stored persistently
   - Fast retrieval (< 100ms for recent items)
   - Reliable data persistence

2. **User Experience**
   - Intuitive history browsing
   - Easy configuration management
   - Smooth visual feedback

3. **Code Quality**
   - 80%+ test coverage
   - All critical paths tested
   - Clean, maintainable code

4. **Performance**
   - No degradation in response time
   - Efficient memory usage
   - Smooth UI interactions

## Risk Mitigation

1. **Database Performance**
   - Implement pagination early
   - Add appropriate indexes
   - Consider SQLite WAL mode

2. **UI Complexity**
   - Start with simple implementations
   - Iterate based on user feedback
   - Keep overlay lightweight

3. **Configuration Security**
   - Use Windows Credential Manager for API keys
   - Never store keys in plain text
   - Implement key rotation support

## Next Steps

1. Create feature branches for each phase
2. Implement database layer first (foundation)
3. Add UI components incrementally
4. Test each feature thoroughly
5. Update documentation as we go

This plan provides a clear roadmap for implementing the missing features while maintaining code quality and user experience.