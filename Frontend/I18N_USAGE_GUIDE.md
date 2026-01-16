# Internationalization (i18n) Usage Guide

## Overview
The NaTourCam application now supports bilingual functionality with English and French languages. Users can toggle between languages using the language switcher button in the navigation bar.

## How It Works

### Language Context
The language system is built using React Context API and is located in `src/contexts/LanguageContext.jsx`. It provides:
- Current language state (`en` or `fr`)
- Translation function `t(key)`
- Language toggle function `toggleLanguage()`
- Language persistence in localStorage

### Using Translations in Components

#### 1. Import the useLanguage hook
```javascript
import { useLanguage } from '../contexts/LanguageContext';
```

#### 2. Get the translation function
```javascript
const { t, language, toggleLanguage } = useLanguage();
```

#### 3. Use the translation function
```javascript
<h1>{t('home.title')}</h1>
<p>{t('home.subtitle')}</p>
<button>{t('common.submit')}</button>
```

### Example Component

```javascript
import React from 'react';
import { useLanguage } from '../contexts/LanguageContext';

const MyComponent = () => {
  const { t } = useLanguage();
  
  return (
    <div>
      <h1>{t('mySection.title')}</h1>
      <p>{t('mySection.description')}</p>
      <button>{t('common.save')}</button>
    </div>
  );
};

export default MyComponent;
```

## Translation Keys Structure

Translations are organized by section in the `LanguageContext.jsx` file:

### Available Translation Sections:
- **nav** - Navigation menu items
- **home** - Homepage content
- **sites** - Tourist sites pages
- **bookings** - Booking-related content
- **profile** - User profile pages
- **auth** - Authentication (login/register)
- **admin** - Admin dashboard
- **common** - Common UI elements (buttons, labels, etc.)
- **footer** - Footer content

### Example Translation Keys:

```javascript
// Navigation
t('nav.home')           // "Home" / "Accueil"
t('nav.sites')          // "Tourist Sites" / "Sites Touristiques"
t('nav.login')          // "Login" / "Connexion"

// Homepage
t('home.title')         // "Discover Cameroon" / "Découvrez le Cameroun"
t('home.subtitle')      // "Explore the beauty..." / "Explorez la beauté..."

// Common
t('common.save')        // "Save" / "Enregistrer"
t('common.cancel')      // "Cancel" / "Annuler"
t('common.loading')     // "Loading..." / "Chargement..."

// Bookings
t('bookings.title')     // "My Bookings" / "Mes Réservations"
t('bookings.status')    // "Status" / "Statut"
```

## Adding New Translations

To add new translations:

1. Open `src/contexts/LanguageContext.jsx`
2. Find the `translations` object at the bottom of the file
3. Add your new keys to both `en` and `fr` objects:

```javascript
const translations = {
  en: {
    myNewSection: {
      title: 'My New Title',
      description: 'My description',
    },
  },
  fr: {
    myNewSection: {
      title: 'Mon Nouveau Titre',
      description: 'Ma description',
    },
  },
};
```

## Language Toggle Button

The language toggle button is located in the Navbar component. It:
- Shows the flag and language code of the opposite language
- Persists the user's language preference in localStorage
- Automatically updates all components when toggled

## Components Already Updated

The following components have been updated to use translations:
- ✅ Navbar
- ✅ Homepage
- ⏳ Footer (to be updated)
- ⏳ Login/Register (to be updated)
- ⏳ Site List (to be updated)
- ⏳ Booking List (to be updated)
- ⏳ Admin Dashboard (to be updated)

## Best Practices

1. **Always use translation keys** instead of hardcoded text
2. **Use descriptive key names** that indicate the content location
3. **Keep translations consistent** across similar UI elements
4. **Test both languages** after adding new content
5. **Avoid concatenating translations** - use complete phrases

### ❌ Bad Practice:
```javascript
<p>{t('common.total')} + ': ' + price}</p>
```

### ✅ Good Practice:
```javascript
<p>{t('common.total')}: {price}</p>
```

## Styling

The language toggle button has custom styling in `App.css`:
```css
.language-toggle {
  background: rgba(255, 255, 255, 0.1);
  padding: 0.5rem 1rem !important;
  border-radius: 6px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  /* ... */
}
```

## Future Enhancements

Potential improvements for the i18n system:
- Add more languages (Spanish, German, etc.)
- Implement lazy loading for translation files
- Add date/time localization
- Add number/currency formatting
- Implement RTL support for Arabic/Hebrew
- Add translation management UI for admins

## Troubleshooting

### Translation not showing
- Check if the key exists in both `en` and `fr` objects
- Verify the key path is correct (e.g., `'section.subsection.key'`)
- Ensure the component imports and uses `useLanguage` hook

### Language not persisting
- Check browser localStorage
- Verify `LanguageProvider` wraps the entire app in `App.jsx`

### Component not re-rendering on language change
- Ensure the component uses the `t` function from `useLanguage` hook
- Check that `LanguageProvider` is properly set up in the component tree

## Support

For questions or issues with the i18n system, please refer to:
- React Context API documentation
- This guide
- The `LanguageContext.jsx` source code
