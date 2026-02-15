
/**
 * Page d'inscription
 * ------------------
 * Composant React pour la création de compte utilisateur.
 * - Fond blanc, texte noir, accents bleus (charte graphique)
 * - Flèche retour en haut à gauche
 * - Formulaire nom, email, mot de passe, confirmation
 * - Boutons sociaux
 */
import React, { useState } from "react";
import { registrationFullSchema } from '../../lib/validation';
import { Link, useNavigate } from "react-router-dom";
import { createUserWithEmailAndPassword, signInWithPopup, GoogleAuthProvider } from "firebase/auth";
import { doc, setDoc, getDoc } from "firebase/firestore";
import { auth, db } from "../../lib/firebase";


const Registration: React.FC = () => {
    // Connexion/inscription avec Google
    const handleGoogleSignup = async () => {
      setError("");
      setSuccess("");
      try {
        const provider = new GoogleAuthProvider();
        const result = await signInWithPopup(auth, provider);
        const user = result.user;

        // Vérifie si le document utilisateur existe déjà dans Firestore
        const userDocRef = doc(db, "users", user.uid);
        const userDocSnap = await getDoc(userDocRef);
        if (!userDocSnap.exists()) {
          // Si l'utilisateur Google est nouveau, crée le document Firestore
          await setDoc(userDocRef, {
            fullname: user.displayName || "",
            email: user.email,
            role: "user",
          });
        }
        setSuccess("Inscription/connexion Google réussie ! Vous allez être redirigé vers l'accueil...");
        setTimeout(() => {
          navigate("/");
        }, 2000);
      } catch (err: any) {
        setError("Erreur Google : " + err.message);
      }
    };
  // États pour les champs et l'erreur
  const [firstName, setFirstName] = useState("");
  const [lastName, setLastName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  const navigate = useNavigate();

  // Soumission du formulaire avec validation yup
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    try {
      // Validation du formulaire avec yup
      // Remplacer par un schéma qui valide prénom et nom séparés (à adapter dans validation.tsx si besoin)
      // await registrationFullSchema.validate({ firstName, lastName, email, password, confirmPassword });

      // Appel API Django pour l'inscription
      const response = await fetch("http://localhost:8000/users/register/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          username: email,
          email,
          first_name: firstName,
          last_name: lastName,
          password,
          password2: confirmPassword
        })
      });
      if (!response.ok) {
        const data = await response.json();
        throw new Error(data?.detail || "Erreur lors de l'inscription");
      }

      setSuccess("Inscription réussie ! Vous allez être redirigé vers l'accueil...");
      setTimeout(() => {
        navigate("/");
      }, 2000); // Redirection après 2 secondes
    } catch (err: any) {
      setError(err.message);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-white text-gray-900 px-4 relative">
      {/* Flèche retour à la page de connexion */}
      <Link to="/" aria-label="Retour à la connexion" title="Retour à la connexion" className="fixed top-4 left-4 z-50 p-2 rounded-full bg-white hover:bg-gray-100 text-blue-600 shadow-md border border-gray-200">
        <svg xmlns="http://www.w3.org/2000/svg" className="w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
          <path d="M15 18l-6-6 6-6" strokeLinecap="round" strokeLinejoin="round" />
        </svg>
      </Link>

      <div className="w-full max-w-md">
        <div className="text-center mb-8">
          {/* Titre principal */}
          <h1 className="text-2xl font-semibold text-gray-900">Créer un compte</h1>
        </div>

        {/* Bloc formulaire d'inscription */}
        <div className="bg-white border border-gray-200 rounded-xl p-6 shadow-lg">
          <form className="space-y-4" onSubmit={handleSubmit}>
            {/* Champ prénom */}
            <div>
              <label htmlFor="firstName" className="block text-sm font-medium text-gray-700 mb-2">Prénom</label>
              <input
                id="firstName"
                name="firstName"
                type="text"
                value={firstName}
                onChange={e => setFirstName(e.target.value)}
                required
                className="block w-full px-4 py-3 rounded-md bg-gray-100 border border-gray-300 text-gray-900 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="Votre prénom"
              />
            </div>
            {/* Champ nom */}
            <div>
              <label htmlFor="lastName" className="block text-sm font-medium text-gray-700 mb-2">Nom</label>
              <input
                id="lastName"
                name="lastName"
                type="text"
                value={lastName}
                onChange={e => setLastName(e.target.value)}
                required
                className="block w-full px-4 py-3 rounded-md bg-gray-100 border border-gray-300 text-gray-900 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="Votre nom"
              />
            </div>
            {/* Champ email */}
            <div>
              <label htmlFor="email" className="block text-sm font-medium text-gray-700 mb-2">Adresse e-mail</label>
              <input
                id="email"
                name="email"
                type="email"
                value={email}
                onChange={e => setEmail(e.target.value)}
                required
                className="block w-full px-4 py-3 rounded-md bg-gray-100 border border-gray-300 text-gray-900 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="votre@email.com"
              />
            </div>
            {/* Champ mot de passe */}
            <div>
              <label htmlFor="password" className="block text-sm font-medium text-gray-700 mb-2">Mot de passe</label>
              <input
                id="password"
                name="password"
                type="password"
                value={password}
                onChange={e => setPassword(e.target.value)}
                required
                className="block w-full px-4 py-3 rounded-md bg-gray-100 border border-gray-300 text-gray-900 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="••••••••"
              />
            </div>
            {/* Champ confirmation mot de passe */}
            <div>
              <label htmlFor="confirmPassword" className="block text-sm font-medium text-gray-700 mb-2">Confirmer le mot de passe</label>
              <input
                id="confirmPassword"
                name="confirmPassword"
                type="password"
                value={confirmPassword}
                onChange={e => setConfirmPassword(e.target.value)}
                required
                className="block w-full px-4 py-3 rounded-md bg-gray-100 border border-gray-300 text-gray-900 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="••••••••"
              />
            </div>
            {/* Affichage du message d'erreur de validation */}
            {error && <div className="text-red-500 text-sm">{error}</div>}
            {/* Affichage du message de succès */}
            {success && <div className="text-green-600 text-sm font-semibold">{success}</div>}
            {/* Bouton s'inscrire */}
            <button
              type="submit"
              className="w-full py-3 rounded-md bg-gradient-to-r from-blue-600 to-blue-400 text-white font-semibold hover:from-blue-700 hover:to-blue-500 transition"
              aria-label="S'inscrire"
            >
              <span className="text-white">S'inscrire</span>
            </button>
          </form>

          {/* Boutons sociaux */}
          <div className="mt-6">
            <div className="flex items-center">
              <div className="flex-grow border-t border-gray-200" />
              <span className="px-4 text-sm text-gray-500">Ou continuer avec</span>
              <div className="flex-grow border-t border-gray-200" />
            </div>
            <div className="mt-4 flex justify-center">
              <button
                type="button"
                className="flex items-center justify-center gap-2 py-2 px-6 rounded-md bg-blue-600 hover:bg-blue-700 transition border border-blue-600"
                aria-label="S'inscrire avec Google"
                onClick={handleGoogleSignup}
              >
                {/* Icône Google */}
                <svg className="w-5 h-5" viewBox="0 0 533.5 544.3" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
                  <path fill="#4285F4" d="M533.5 278.4c0-23.4-1.9-46.1-5.7-68.1H272v128.8h147.1c-6.4 34.9-25.4 64.4-54.2 84.1l87.4 67c51-46.9 82.2-116.3 82.2-211.8z"/>
                  <path fill="#34A853" d="M272 544.3c73.6 0 135.5-24.3 180.7-66.2l-87.4-67c-24.2 16.3-55.1 26-93.3 26-71.7 0-132.4-48.3-154.1-113.1l-89.8 69.4C72.2 481 165.8 544.3 272 544.3z"/>
                  <path fill="#FBBC05" d="M117.9 328.8c-10.9-32.6-10.9-67.6 0-100.2L28.1 159.2C-8.6 221.6-8.6 322.8 28.1 385.1l89.8-69.4z"/>
                  <path fill="#EA4335" d="M272 109.2c39.9 0 75.8 13.7 104 40.6l78-78C398.1 24.4 336.2 0 272 0 165.8 0 72.2 63.3 28.1 159.2l89.8 69.4C139.6 157.5 200.3 109.2 272 109.2z"/>
                </svg>
                <span className="text-sm text-white">Google</span>
              </button>
            </div>
          </div>
        </div>
        <p className="mt-6 text-center text-sm text-gray-500">Déjà un compte ? <Link to="/login" className="text-blue-600 hover:text-blue-500">Connectez-vous ici</Link></p>
      </div>
    </div>
  );
};

export default Registration;