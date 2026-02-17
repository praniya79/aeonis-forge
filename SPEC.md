# AeonForge Streaming Site Specification

## Project Overview
- **Project Name**: AeonForge Streaming Site
- **Type**: Real-time streaming web application
- **Core Functionality**: Display meta-simulation narratives in human-readable form
- **Target Users**: Visitors interested in AI meta-simulation content

## UI/UX Specification

### Layout Structure
- **Header**: Fixed top navigation with logo and live status
- **Hero**: Full-viewport with animated background and live indicator
- **Narrative Stream**: Real-time scrolling feed of simulation events
- **Agent Panel**: Grid showing active simulation agents
- **Footer**: Minimal footer with links

### Responsive Breakpoints
- Mobile: < 768px
- Tablet: 768px - 1024px
- Desktop: > 1024px

### Visual Design

#### Color Palette
- **Background**: `#030408` (deep space black)
- **Surface**: `#0A0E17` (dark navy)
- **Card**: `#121A2B` (dark blue-gray)
- **Primary Accent**: `#7C3AED` (electric violet)
- **Secondary Accent**: `#06B6D4` (cyan)
- **Success**: `#10B981` (emerald)
- **Warning**: `#F59E0B` (amber)
- **Text Primary**: `#F8FAFC` (off-white)
- **Text Secondary**: `#94A3B8` (slate)
- **Border**: `#1E293B` (dark border)

#### Typography
- **Display Font**: "Orbitron" (futuristic headers)
- **Body Font**: "Inter" (readable body text)
- **Monospace**: "JetBrains Mono" (code/data)

#### Visual Effects
- Subtle gradient overlays
- Glowing borders on hover
- Smooth fade-in animations
- Pulsing live indicator

### Components

1. **LiveIndicator**
   - Pulsing red dot with "LIVE" text
   - Animation: pulse 2s infinite

2. **NarrativeCard**
   - Timestamp, event type, description
   - Hover: subtle glow effect

3. **AgentCard**
   - Agent name, status, activity
   - Color-coded status indicator

4. **StreamFeed**
   - Auto-scrolling narrative list
   - Maximum 50 visible items
   - New items slide in from top

## Functionality Specification

### Core Features
1. **Real-time Narrative Display**
   - Fetch from /api/stream endpoint
   - Auto-refresh every 5 seconds
   - Smooth scroll animations

2. **Live Status Indicator**
   - Shows if simulation is active
   - Connection status

3. **Agent Status Panel**
   - Display 7 agents with status
   - Activity updates

4. **Dark Theme Default**
   - Automatic dark mode
   - Optimized for low light

### Data Handling
- Client-side polling for updates
- Local state management
- Error handling for connection failures

### Edge Cases
- Handle API unavailability gracefully
- Show loading states
- Display connection errors

## Acceptance Criteria
- [x] Page loads with dark futuristic theme
- [x] Live indicator animates correctly
- [x] Narrative feed displays and auto-refreshes
- [x] Agent status panel shows 7 agents
- [x] Responsive on mobile/tablet/desktop
- [x] No console errors on load
