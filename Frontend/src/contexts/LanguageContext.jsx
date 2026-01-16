import React, { createContext, useContext, useState, useEffect } from 'react';

const LanguageContext = createContext();

export const useLanguage = () => {
  const context = useContext(LanguageContext);
  if (!context) {
    throw new Error('useLanguage must be used within a LanguageProvider');
  }
  return context;
};

export const LanguageProvider = ({ children }) => {
  const [language, setLanguage] = useState(() => {
    // Get language from localStorage or default to English
    return localStorage.getItem('language') || 'en';
  });

  useEffect(() => {
    // Save language preference to localStorage
    localStorage.setItem('language', language);
  }, [language]);

  const toggleLanguage = () => {
    setLanguage(prev => prev === 'en' ? 'fr' : 'en');
  };

  const t = (key) => {
    // Get translation from the translations object
    const keys = key.split('.');
    let value = translations[language];
    
    for (const k of keys) {
      value = value?.[k];
    }
    
    return value || key;
  };

  const value = {
    language,
    setLanguage,
    toggleLanguage,
    t,
  };

  return (
    <LanguageContext.Provider value={value}>
      {children}
    </LanguageContext.Provider>
  );
};

// Translation object
const translations = {
  en: {
    // Navigation
    nav: {
      home: 'Home',
      sites: 'Tourist Sites',
      bookings: 'My Bookings',
      profile: 'Profile',
      admin: 'Admin Dashboard',
      login: 'Login',
      register: 'Register',
      logout: 'Logout',
    },
    
    // Homepage
    home: {
      title: 'Discover Cameroon',
      subtitle: 'Explore the beauty and culture of Cameroon',
      description: 'From pristine beaches to majestic mountains, discover the hidden gems of Cameroon',
      exploreButton: 'Explore Sites',
      featuredSites: 'Featured Tourist Sites',
      whyChoose: 'Why Choose NaTourCam?',
      authenticExperiences: 'Authentic Experiences',
      authenticDesc: 'Discover genuine Cameroonian culture and traditions',
      expertGuides: 'Expert Guides',
      expertDesc: 'Professional guides with deep local knowledge',
      easyBooking: 'Easy Booking',
      easyDesc: 'Simple and secure online booking process',
      safeTravel: 'Safe Travel',
      safeDesc: 'Your safety is our top priority',
    },
    
    // Sites
    sites: {
      title: 'Tourist Sites',
      search: 'Search sites...',
      filter: 'Filter',
      allRegions: 'All Regions',
      sortBy: 'Sort by',
      name: 'Name',
      price: 'Price',
      rating: 'Rating',
      noSites: 'No tourist sites found',
      loading: 'Loading sites...',
      entranceFee: 'Entrance Fee',
      viewDetails: 'View Details',
      bookNow: 'Book Now',
      region: 'Region',
      description: 'Description',
      location: 'Location',
      openingHours: 'Opening Hours',
      facilities: 'Facilities',
      reviews: 'Reviews',
      gallery: 'Gallery',
    },
    
    // Bookings
    bookings: {
      title: 'My Bookings',
      noBookings: 'No bookings found',
      bookingDate: 'Booking Date',
      visitors: 'Visitors',
      totalPrice: 'Total Price',
      status: 'Status',
      pending: 'Pending',
      confirmed: 'Confirmed',
      completed: 'Completed',
      cancelled: 'Cancelled',
      cancel: 'Cancel',
      viewDetails: 'View Details',
      createBooking: 'Create Booking',
      selectSite: 'Select Site',
      selectDate: 'Select Date',
      numberOfVisitors: 'Number of Visitors',
      specialRequests: 'Special Requests',
      submit: 'Submit Booking',
      confirmCancel: 'Are you sure you want to cancel this booking?',
    },
    
    // Profile
    profile: {
      title: 'My Profile',
      personalInfo: 'Personal Information',
      firstName: 'First Name',
      lastName: 'Last Name',
      email: 'Email',
      username: 'Username',
      phoneNumber: 'Phone Number',
      dateOfBirth: 'Date of Birth',
      nationality: 'Nationality',
      address: 'Address',
      city: 'City',
      country: 'Country',
      save: 'Save Changes',
      cancel: 'Cancel',
      edit: 'Edit Profile',
      changePassword: 'Change Password',
      currentPassword: 'Current Password',
      newPassword: 'New Password',
      confirmPassword: 'Confirm Password',
      updateSuccess: 'Profile updated successfully',
      updateError: 'Failed to update profile',
    },
    
    // Auth
    auth: {
      login: 'Login',
      register: 'Register',
      email: 'Email',
      password: 'Password',
      confirmPassword: 'Confirm Password',
      firstName: 'First Name',
      lastName: 'Last Name',
      username: 'Username',
      forgotPassword: 'Forgot Password?',
      noAccount: "Don't have an account?",
      hasAccount: 'Already have an account?',
      signUp: 'Sign Up',
      signIn: 'Sign In',
      loginSuccess: 'Login successful',
      loginError: 'Login failed',
      registerSuccess: 'Registration successful',
      registerError: 'Registration failed',
      logoutSuccess: 'Logout successful',
    },
    
    // Admin Dashboard
    admin: {
      title: 'Admin Dashboard',
      subtitle: 'Manage your tourism platform',
      overview: 'Overview',
      sites: 'Tourist Sites',
      bookings: 'Bookings',
      users: 'Users',
      totalSites: 'Tourist Sites',
      totalBookings: 'Total Bookings',
      totalUsers: 'Registered Users',
      totalRevenue: 'Total Revenue',
      active: 'active',
      pending: 'pending',
      recentBookings: 'Recent Bookings',
      popularSites: 'Popular Sites',
      manageSites: 'Manage Tourist Sites',
      manageBookings: 'Manage Bookings',
      manageUsers: 'Manage Users',
      addNewSite: 'Add New Site',
      edit: 'Edit',
      view: 'View',
      delete: 'Delete',
      activate: 'Activate',
      deactivate: 'Deactivate',
      searchUsers: 'Search users...',
      all: 'All',
      confirmed: 'Confirmed',
      completed: 'Completed',
      cancelled: 'Cancelled',
      name: 'Name',
      region: 'Region',
      entranceFee: 'Entrance Fee',
      status: 'Status',
      images: 'Images',
      actions: 'Actions',
      id: 'ID',
      site: 'Site',
      date: 'Date',
      visitors: 'Visitors',
      totalPrice: 'Total Price',
      joined: 'Joined',
      verified: 'Verified',
      staff: 'Staff',
      superuser: 'Admin',
    },
    
    // Common
    common: {
      loading: 'Loading...',
      error: 'Error',
      success: 'Success',
      save: 'Save',
      cancel: 'Cancel',
      delete: 'Delete',
      edit: 'Edit',
      view: 'View',
      close: 'Close',
      submit: 'Submit',
      search: 'Search',
      filter: 'Filter',
      sort: 'Sort',
      back: 'Back',
      next: 'Next',
      previous: 'Previous',
      yes: 'Yes',
      no: 'No',
      confirm: 'Confirm',
      total: 'Total',
      from: 'From',
      to: 'To',
      date: 'Date',
      time: 'Time',
      price: 'Price',
      currency: 'FCFA',
    },
    
    // Footer
    footer: {
      about: 'About NaTourCam',
      aboutDesc: 'Discover the beauty and culture of Cameroon with our curated tourist experiences.',
      quickLinks: 'Quick Links',
      contact: 'Contact Us',
      email: 'Email',
      phone: 'Phone',
      address: 'Address',
      followUs: 'Follow Us',
      rights: 'All rights reserved',
      privacy: 'Privacy Policy',
      terms: 'Terms of Service',
    },
  },
  
  fr: {
    // Navigation
    nav: {
      home: 'Accueil',
      sites: 'Sites Touristiques',
      bookings: 'Mes Réservations',
      profile: 'Profil',
      admin: 'Tableau de Bord Admin',
      login: 'Connexion',
      register: 'Inscription',
      logout: 'Déconnexion',
    },
    
    // Homepage
    home: {
      title: 'Découvrez le Cameroun',
      subtitle: 'Explorez la beauté et la culture du Cameroun',
      description: 'Des plages immaculées aux montagnes majestueuses, découvrez les joyaux cachés du Cameroun',
      exploreButton: 'Explorer les Sites',
      featuredSites: 'Sites Touristiques en Vedette',
      whyChoose: 'Pourquoi Choisir NaTourCam?',
      authenticExperiences: 'Expériences Authentiques',
      authenticDesc: 'Découvrez la véritable culture et traditions camerounaises',
      expertGuides: 'Guides Experts',
      expertDesc: 'Guides professionnels avec une connaissance locale approfondie',
      easyBooking: 'Réservation Facile',
      easyDesc: 'Processus de réservation en ligne simple et sécurisé',
      safeTravel: 'Voyage Sûr',
      safeDesc: 'Votre sécurité est notre priorité absolue',
    },
    
    // Sites
    sites: {
      title: 'Sites Touristiques',
      search: 'Rechercher des sites...',
      filter: 'Filtrer',
      allRegions: 'Toutes les Régions',
      sortBy: 'Trier par',
      name: 'Nom',
      price: 'Prix',
      rating: 'Note',
      noSites: 'Aucun site touristique trouvé',
      loading: 'Chargement des sites...',
      entranceFee: "Frais d'Entrée",
      viewDetails: 'Voir Détails',
      bookNow: 'Réserver Maintenant',
      region: 'Région',
      description: 'Description',
      location: 'Emplacement',
      openingHours: "Heures d'Ouverture",
      facilities: 'Installations',
      reviews: 'Avis',
      gallery: 'Galerie',
    },
    
    // Bookings
    bookings: {
      title: 'Mes Réservations',
      noBookings: 'Aucune réservation trouvée',
      bookingDate: 'Date de Réservation',
      visitors: 'Visiteurs',
      totalPrice: 'Prix Total',
      status: 'Statut',
      pending: 'En Attente',
      confirmed: 'Confirmé',
      completed: 'Terminé',
      cancelled: 'Annulé',
      cancel: 'Annuler',
      viewDetails: 'Voir Détails',
      createBooking: 'Créer une Réservation',
      selectSite: 'Sélectionner un Site',
      selectDate: 'Sélectionner une Date',
      numberOfVisitors: 'Nombre de Visiteurs',
      specialRequests: 'Demandes Spéciales',
      submit: 'Soumettre la Réservation',
      confirmCancel: 'Êtes-vous sûr de vouloir annuler cette réservation?',
    },
    
    // Profile
    profile: {
      title: 'Mon Profil',
      personalInfo: 'Informations Personnelles',
      firstName: 'Prénom',
      lastName: 'Nom',
      email: 'Email',
      username: "Nom d'Utilisateur",
      phoneNumber: 'Numéro de Téléphone',
      dateOfBirth: 'Date de Naissance',
      nationality: 'Nationalité',
      address: 'Adresse',
      city: 'Ville',
      country: 'Pays',
      save: 'Enregistrer les Modifications',
      cancel: 'Annuler',
      edit: 'Modifier le Profil',
      changePassword: 'Changer le Mot de Passe',
      currentPassword: 'Mot de Passe Actuel',
      newPassword: 'Nouveau Mot de Passe',
      confirmPassword: 'Confirmer le Mot de Passe',
      updateSuccess: 'Profil mis à jour avec succès',
      updateError: 'Échec de la mise à jour du profil',
    },
    
    // Auth
    auth: {
      login: 'Connexion',
      register: 'Inscription',
      email: 'Email',
      password: 'Mot de Passe',
      confirmPassword: 'Confirmer le Mot de Passe',
      firstName: 'Prénom',
      lastName: 'Nom',
      username: "Nom d'Utilisateur",
      forgotPassword: 'Mot de passe oublié?',
      noAccount: "Vous n'avez pas de compte?",
      hasAccount: 'Vous avez déjà un compte?',
      signUp: "S'inscrire",
      signIn: 'Se Connecter',
      loginSuccess: 'Connexion réussie',
      loginError: 'Échec de la connexion',
      registerSuccess: 'Inscription réussie',
      registerError: "Échec de l'inscription",
      logoutSuccess: 'Déconnexion réussie',
    },
    
    // Admin Dashboard
    admin: {
      title: 'Tableau de Bord Admin',
      subtitle: 'Gérez votre plateforme touristique',
      overview: 'Aperçu',
      sites: 'Sites Touristiques',
      bookings: 'Réservations',
      users: 'Utilisateurs',
      totalSites: 'Sites Touristiques',
      totalBookings: 'Total des Réservations',
      totalUsers: 'Utilisateurs Inscrits',
      totalRevenue: 'Revenu Total',
      active: 'actif',
      pending: 'en attente',
      recentBookings: 'Réservations Récentes',
      popularSites: 'Sites Populaires',
      manageSites: 'Gérer les Sites Touristiques',
      manageBookings: 'Gérer les Réservations',
      manageUsers: 'Gérer les Utilisateurs',
      addNewSite: 'Ajouter un Nouveau Site',
      edit: 'Modifier',
      view: 'Voir',
      delete: 'Supprimer',
      activate: 'Activer',
      deactivate: 'Désactiver',
      searchUsers: 'Rechercher des utilisateurs...',
      all: 'Tous',
      confirmed: 'Confirmé',
      completed: 'Terminé',
      cancelled: 'Annulé',
      name: 'Nom',
      region: 'Région',
      entranceFee: "Frais d'Entrée",
      status: 'Statut',
      images: 'Images',
      actions: 'Actions',
      id: 'ID',
      site: 'Site',
      date: 'Date',
      visitors: 'Visiteurs',
      totalPrice: 'Prix Total',
      joined: 'Inscrit',
      verified: 'Vérifié',
      staff: 'Personnel',
      superuser: 'Admin',
    },
    
    // Common
    common: {
      loading: 'Chargement...',
      error: 'Erreur',
      success: 'Succès',
      save: 'Enregistrer',
      cancel: 'Annuler',
      delete: 'Supprimer',
      edit: 'Modifier',
      view: 'Voir',
      close: 'Fermer',
      submit: 'Soumettre',
      search: 'Rechercher',
      filter: 'Filtrer',
      sort: 'Trier',
      back: 'Retour',
      next: 'Suivant',
      previous: 'Précédent',
      yes: 'Oui',
      no: 'Non',
      confirm: 'Confirmer',
      total: 'Total',
      from: 'De',
      to: 'À',
      date: 'Date',
      time: 'Heure',
      price: 'Prix',
      currency: 'FCFA',
    },
    
    // Footer
    footer: {
      about: 'À Propos de NaTourCam',
      aboutDesc: 'Découvrez la beauté et la culture du Cameroun avec nos expériences touristiques organisées.',
      quickLinks: 'Liens Rapides',
      contact: 'Contactez-Nous',
      email: 'Email',
      phone: 'Téléphone',
      address: 'Adresse',
      followUs: 'Suivez-Nous',
      rights: 'Tous droits réservés',
      privacy: 'Politique de Confidentialité',
      terms: "Conditions d'Utilisation",
    },
  },
};
