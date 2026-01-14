# NaTourCam Frontend

This is the frontend application for the NaTourCam tourism platform, built with React.js.

## Features

- User authentication (login/register)
- Browse tourist sites
- View detailed site information
- Book visits to tourist sites
- User dashboard with booking summary

## Technologies Used

- React.js
- React Router
- Axios for API communication
- CSS3 for styling

## Prerequisites

- Node.js (version 14 or higher)
- npm (comes with Node.js)

## Setup Instructions

1. Clone the repository
2. Navigate to the frontend directory:
   ```
   cd frontend
   ```
3. Install dependencies:
   ```
   npm install
   ```
4. Start the development server:
   ```
   npm run dev
   ```

The application will be available at `http://localhost:3000`.

## Project Structure

```
src/
├── components/
│   ├── auth/          # Authentication components (Login, Register, Logout)
│   ├── bookings/      # Booking-related components
│   ├── dashboard/     # User dashboard components
│   └── tourism/       # Tourism site components
├── contexts/          # React contexts (AuthContext)
├── services/          # API service layer
├── App.jsx            # Main application component
└── main.jsx           # Entry point
```

## API Integration

The frontend communicates with the Django backend API at `http://localhost:8000/api/`.

Key API endpoints used:
- Authentication: `/api/auth/`
- Tourism sites: `/api/tourism/`
- Bookings: `/api/bookings/`

## Development

To start the development server:
```
npm run dev
```

To build for production:
```
npm run build
```

To preview the production build:
```
npm run preview
