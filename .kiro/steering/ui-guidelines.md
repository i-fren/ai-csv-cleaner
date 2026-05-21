---
inclusion: auto
---

# UI Guidelines — DataDoctor AI

## Design System

### Color Palette
- Background: `#0a0a1a` (deep navy)
- Card background: `white/5` with `border-white/10`
- Primary gradient: `from-blue-600 to-purple-600`
- Text primary: `text-white`
- Text secondary: `text-gray-400`
- Success: `text-green-400`, `bg-green-500/10`
- Warning: `text-yellow-400`, `bg-yellow-500/10`
- Error: `text-red-400`, `bg-red-500/10`
- Accent: `text-blue-400`, `text-purple-400`

### Typography
- Headings: `font-bold text-white`
- Body: `text-sm text-gray-400`
- Labels: `text-xs text-gray-400 uppercase tracking-wide`
- Metric values: `text-2xl font-bold text-white`

### Spacing
- Card padding: `p-6`
- Section gaps: `space-y-6`
- Grid gaps: `gap-4` or `gap-6`
- Inner element spacing: `mb-2`, `mb-4`

### Components

#### Cards
```
rounded-2xl bg-white/5 border border-white/10 p-6
```

#### Buttons (Primary)
```
px-5 py-3 rounded-xl bg-gradient-to-r from-blue-600 to-purple-600 
hover:from-blue-500 hover:to-purple-500 text-white font-medium text-sm 
transition-all duration-200
```

#### Buttons (Secondary)
```
px-4 py-2 rounded-xl bg-white/5 border border-white/10 
text-gray-300 hover:bg-white/10 hover:text-white transition-all duration-200
```

#### Inputs
```
bg-white/5 border border-white/10 rounded-xl px-4 py-3 text-sm text-white 
placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500/50
```

#### Status Badges
```
px-3 py-1.5 rounded-full bg-white/5 border border-white/10 text-xs text-gray-400
```

### Animations
- Panel transitions: `transition-all duration-200`
- Hover effects: `hover:scale-105 transition-transform duration-200`
- Background orbs: `animate-pulse-slow` with `blur-3xl`
- Loading: `animate-bounce` with staggered delays

### Responsive Breakpoints
- Mobile: default (full-width single column)
- Tablet: `sm:` (640px+)
- Desktop: `lg:` (1024px+)
- Wide: `xl:` (1280px+)

### Accessibility Requirements
- All interactive elements MUST have `aria-label` attributes
- Tables MUST have `aria-label` and `<th scope="col">`
- Loading states MUST have `role="status"` and `aria-label="Loading"`
- Error banners MUST have `role="alert"`
- Navigation tabs MUST have `role="tab"` and `aria-selected`
- Minimum contrast ratio: 4.5:1 for all text
- Focus indicators must be visible

### Layout Patterns
- Max content width: `max-w-7xl mx-auto`
- Page padding: `px-4 sm:px-6 lg:px-8`
- Sticky header with backdrop blur: `sticky top-0 bg-[#0a0a1a]/80 backdrop-blur-xl`
- Navigation below header with horizontal scroll on mobile
