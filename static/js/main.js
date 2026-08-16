document.addEventListener('DOMContentLoaded', () => {
    const toggle = document.getElementById('themeToggle');
    const langToggle = document.getElementById('langToggle');
    const root = document.body;
    const navToggle = document.querySelector('.nav-toggle');
    const navLinks = document.querySelector('.nav-links');

    const translations = {
        en: {
            navFeatures: 'Features',
            navTips: 'Safety Tips',
            navLogin: 'Login',
            navRegister: 'Register',
            navDashboard: 'Dashboard',
            navSos: 'SOS',
            navRoutes: 'Routes',
            navLive: 'Live Sharing',
            navContacts: 'Contacts',
            navProfile: 'Profile',
            navLogout: 'Logout',
            heroTitle: 'SafeStride',
            heroText: 'Helping girls and women travel with confidence through instant alerts, trusted contacts, and smart safety guidance.',
            heroStart: 'Start Protecting Yourself',
            heroHow: 'See How It Works',
            sectionWhy: 'Why SafeStride Matters for Girls',
            feature1Title: 'Quick SOS Alerts',
            feature1Text: 'Send urgent help requests instantly with your current location to trusted people.',
            feature2Title: 'Safer Route Planning',
            feature2Text: 'Choose safer travel routes and stay informed during every step of your journey.',
            feature3Title: 'Trusted Contact Support',
            feature3Text: 'Keep emergency contacts ready so help is always just one tap away.',
            tipsTitle: 'Girls Safety Tips',
            tip1Title: 'Share Your Journey',
            tip1Text: 'Let someone know when you leave, the route you are taking, and when you reach home safely.',
            tip2Title: 'Stay Alert',
            tip2Text: 'Be mindful of your surroundings, especially during late evenings or unfamiliar places.',
            tip3Title: 'Keep Help Nearby',
            tip3Text: 'Save trusted contacts and make sure your emergency support options are always ready.',
            footerNote: 'Empowering girls and women with safety, confidence, and support.',
            welcomeBack: 'Welcome Back',
            loginText: 'Login to access your safety dashboard.',
            loginEmail: 'Email',
            loginPassword: 'Password',
            loginButton: 'Login',
            noAccount: "Don't have an account?",
            registerText: 'Join SafeStride to protect your travel.',
            registerTitle: 'Create Account',
            registerFullName: 'Full Name',
            registerPhone: 'Phone',
            registerConfirm: 'Confirm Password',
            registerButton: 'Register',
            haveAccount: 'Already have an account?',
            dashboardWelcome: 'Welcome',
            safetyScore: 'Safety Score',
            currentLocation: 'Current Location',
            loadingMap: 'Loading map...',
            checkingLocation: 'Checking location...',
            locationStatus: 'Checking location...',
            coordsLabel: '--',
            emergencySOS: 'Emergency SOS',
            sosDescription: 'Send instant help with one click.',
            quickAccess: 'Quick Access',
            emergencyContacts: 'Emergency Contacts',
            recentAlerts: 'Recent Alerts',
            footerAlways: 'Always stay connected to safety.',
            saveContact: 'Save Contact',
            addContact: 'Add Contact',
            savedContacts: 'Saved Contacts',
            contactName: 'Name',
            contactPhone: 'Phone',
            contactRelation: 'Relation',
            profileTitle: 'My Profile',
            profileSave: 'Save Profile',
            profileAddress: 'Address',
            routeTitle: 'Safe Route Finder',
            routeDescription: 'Use your live location and destination to view a safer route and nearby support areas.',
            routeLive: 'Live Location',
            routeDestination: 'Destination',
            routeShow: 'Show Safe Route',
            routeReset: 'Reset',
            routeUseLive: 'Use My Live Location',
            routeLivePlaceholder: 'Auto-detected or enter a start point',
            routeDestinationPlaceholder: 'Enter your destination',
            routeSummaryDefault: 'Waiting for your location...',
            liveTitle: 'Live Location Sharing',
            sosTitle: 'Emergency SOS',
            sosDescription2: 'Trigger an alert immediately and notify your contacts with your exact location.',
            sosPlaceholder: 'Write a short emergency message...',
            sosButton: 'Trigger SOS',
            liveStatus: 'Live Status',
            mapPlaceholder: 'Location map will appear here.'
        },
        ta: {
            navFeatures: 'விசேஷங்கள்',
            navTips: 'பாதுகாப்பு குறிப்புகள்',
            navLogin: 'உள்நுழை',
            navRegister: 'பதிவு',
            navDashboard: 'டாஷ்போர்ட்',
            navSos: 'SOS',
            navRoutes: 'வழிகள்',
            navLive: 'நேரடி பகிர்வு',
            navContacts: 'தொடர்புகள்',
            navProfile: 'சுயவிவரம்',
            navLogout: 'வெளியேறு',
            heroTitle: 'SafeStride',
            heroText: 'அவசர எச்சரிக்கைகள், நம்பகமான தொடர்புகள் மற்றும் புத்திசாலித்தனமான பாதுகாப்பு வழிமுறைகள் மூலம் சிறுமிகளும் பெண்களும் தன்னம்பிக்கையுடன் பயணம் செய்ய உதவுகிறோம்.',
            heroStart: 'உங்களைப் பாதுகாத்துக் கொள்ளத் தொடங்குங்கள்',
            heroHow: 'இது எப்படி வேலை செய்கிறது',
            sectionWhy: 'சிறுமிகளுக்காக SafeStride ஏன் முக்கியம்',
            feature1Title: 'விரைவு SOS எச்சரிக்கைகள்',
            feature1Text: 'உங்கள் இப்போதைய இருப்பிடத்துடன் நம்பகமான மக்களுக்கு உடனடி உதவி கோரிக்கைகளை அனுப்பவும்.',
            feature2Title: 'பாதுகாப்பான வழி திட்டமிடல்',
            feature2Text: 'பாதுகாப்பான பயண வழிகளை தேர்வு செய்து, உங்கள் பயணத்தின் ஒவ்வொரு கட்டத்திலும் தகவலறிந்தவர்களாக இருங்கள்.',
            feature3Title: 'நம்பகமான தொடர்பு ஆதரவு',
            feature3Text: 'அவசர தொடர்புகளை தயார் நிலையில் வைத்திருங்கள், உதவி எப்போதும் ஒரு தட்டில் கிடைக்கும்.',
            tipsTitle: 'சிறுமிகளுக்கான பாதுகாப்பு குறிப்புகள்',
            tip1Title: 'உங்கள் பயணத்தை பகிருங்கள்',
            tip1Text: 'நீங்கள் எப்போது வெளியேறுகிறீர்கள், எந்த வழியில் செல்கிறீர்கள், எப்போது வீட்டிற்கு safely வந்து சேர்கிறீர்கள் என்பதை யாராவது அறிந்திருக்கச் செய்யுங்கள்.',
            tip2Title: 'கவனமாக இருங்கள்',
            tip2Text: 'குற especially மாலை நேரங்களில் அல்லது unfamiliar இடங்களில் உங்கள் சுற்றுப்புறங்களை கவனத்தில் கொள்ளுங்கள்.',
            tip3Title: 'உதவியை அருகில் வைத்திருங்கள்',
            tip3Text: 'நம்பகமான தொடர்புகளை சேமித்து, உங்கள் அவசர ஆதரவு விருப்பங்கள் எப்போதும் தயாராக உள்ளன என்பதை உறுதிப்படுத்திக் கொள்ளுங்கள்.',
            footerNote: 'பாதுகாப்பு, தன்னம்பிக்கை மற்றும் ஆதரவுடன் சிறுமிகளையும் பெண்களையும் பலப்படுத்துதல்.',
            welcomeBack: 'மீண்டும் வரவேற்கிறோம்',
            loginText: 'உங்கள் பாதுகாப்பு டாஷ்போர்டுக்குள் நுழைய உள்நுழையுங்கள்.',
            loginEmail: 'மின்னஞ்சல்',
            loginPassword: 'கடவுச்சொல்',
            loginButton: 'உள்நுழை',
            noAccount: 'கணக்கு இல்லையா?',
            registerText: 'உங்கள் பயணத்தை பாதுகாக்க SafeStride இல் சேருங்கள்.',
            registerTitle: 'கணக்கு உருவாக்கு',
            registerFullName: 'முழுப் பெயர்',
            registerPhone: 'தொலைபேசி',
            registerConfirm: 'கடவுச்சொல்லை உறுதிப்படுத்து',
            registerButton: 'பதிவு',
            haveAccount: 'ஏற்கனவே கணக்கு இருக்கிறதா?',
            dashboardWelcome: 'வரவேற்கிறோம்',
            safetyScore: 'பாதுகாப்பு மதிப்பெண்',
            currentLocation: 'தற்போதைய இடம்',
            loadingMap: 'வரைபடம் ஏற்றப்படுகிறது...',
            checkingLocation: 'இருப்பிடம் சரிபார்க்கப்படுகிறது...',
            locationStatus: 'இருப்பிடம் சரிபார்க்கப்படுகிறது...',
            coordsLabel: '--',
            emergencySOS: 'அவசர SOS',
            sosDescription: 'ஒரே கிளிக்கில் உடனடி உதவியை அனுப்பவும்.',
            quickAccess: 'விரைவு அணுகல்',
            emergencyContacts: 'அவசர தொடர்புகள்',
            recentAlerts: 'சமீப எச்சரிக்கைகள்',
            footerAlways: 'பாதுகாப்புடன் இணைந்திருக்க எப்போதும் தயாராக இருங்கள்.',
            saveContact: 'தொடர்பை சேமி',
            addContact: 'தொடர்பு சேர்க்கவும்',
            savedContacts: 'சேமிக்கப்பட்ட தொடர்புகள்',
            contactName: 'பெயர்',
            contactPhone: 'தொலைபேசி',
            contactRelation: 'உறவு',
            profileTitle: 'என் சுயவிவரம்',
            profileSave: 'சுயவிவரத்தை சேமி',
            profileAddress: 'முகவரி',
            routeTitle: 'பாதுகாப்பான வழி கண்டுபிடிப்பான்',
            routeDescription: 'உங்கள் நேரடி இருப்பிடத்தையும் இலக்கையும் பயன்படுத்தி பாதுகாப்பான வழி மற்றும் அருகிலுள்ள ஆதரவு பகுதிகளைக் காணுங்கள்.',
            routeLive: 'நேரடி இருப்பிடம்',
            routeDestination: 'இலக்கு',
            routeShow: 'பாதுகாப்பான வழி காட்டு',
            routeReset: 'மீட்டமை',
            routeUseLive: 'என் நேரடி இருப்பிடத்தை பயன்படுத்து',
            routeLivePlaceholder: 'தானாக கண்டறியப்பட்ட அல்லது தொடக்க இடத்தை உள்ளிடவும்',
            routeDestinationPlaceholder: 'உங்கள் இலக்கை உள்ளிடவும்',
            routeSummaryDefault: 'உங்கள் இருப்பிடத்திற்காக காத்திருக்கிறது...',
            liveTitle: 'நேரடி இருப்பிட பகிர்வு',
            sosTitle: 'அவசர SOS',
            sosDescription2: 'உங்கள் இருப்பிடத்துடன் உடனடியாக விழிப்பூட்டலைத் தொடங்குங்கள்.',
            sosPlaceholder: 'குறுகிய அவசர செய்தியை எழுதுங்கள்...',
            sosButton: 'SOS செய்',
            liveStatus: 'நேரடி நிலை',
            mapPlaceholder: 'இருப்பிட வரைபடம் இங்கே தோன்றும்.'
        }
    };

    let currentLanguage = localStorage.getItem('safestride-language') === 'ta' ? 'ta' : 'en';

    function setLanguage(lang) {
        currentLanguage = lang;
        const current = translations[lang] || translations.en;
        document.documentElement.lang = lang;
        document.querySelectorAll('[data-i18n]').forEach((el) => {
            const key = el.dataset.i18n;
            if (current[key]) {
                el.textContent = current[key];
            }
        });
        document.querySelectorAll('[data-i18n-placeholder]').forEach((el) => {
            const key = el.dataset.i18nPlaceholder;
            if (current[key]) {
                el.placeholder = current[key];
            }
        });
        if (langToggle) {
            langToggle.textContent = lang === 'en' ? 'தமிழ்' : 'EN';
            langToggle.setAttribute('aria-label', lang === 'en' ? 'Switch to Tamil' : 'Switch to English');
        }
        localStorage.setItem('safestride-language', lang);
    }

    if (langToggle) {
        langToggle.addEventListener('click', () => {
            const nextLanguage = currentLanguage === 'en' ? 'ta' : 'en';
            setLanguage(nextLanguage);
        });
    }

    setLanguage(currentLanguage);

    if (navToggle && navLinks) {
        navToggle.addEventListener('click', () => {
            navLinks.classList.toggle('active');
        });

        document.addEventListener('click', (e) => {
            if (!e.target.closest('.nav-menu')) {
                navLinks.classList.remove('active');
            }
        });
    }

    if (toggle) {
        const isDark = localStorage.getItem('safestride-theme') === 'dark';
        if (isDark) {
            root.classList.add('dark-theme');
            toggle.textContent = '☀️';
        }

        toggle.addEventListener('click', () => {
            root.classList.toggle('dark-theme');
            const dark = root.classList.contains('dark-theme');
            toggle.textContent = dark ? '☀️' : '🌙';
            localStorage.setItem('safestride-theme', dark ? 'dark' : 'light');
        });
    }

    const year = document.getElementById('year');
    if (year) {
        year.textContent = new Date().getFullYear();
    }

    const statusText = document.getElementById('locationStatus');
    const coordsText = document.getElementById('coordsValue');
    const mapBox = document.getElementById('mapBox');

    function updateMap(lat, lng) {
        if (coordsText) {
            coordsText.textContent = `${lat.toFixed(4)}, ${lng.toFixed(4)}`;
        }

        if (mapBox) {
            const mapUrl = `https://maps.google.com/maps?q=${lat},${lng}&z=15&output=embed`;
            mapBox.innerHTML = `<iframe title="Live location map" src="${mapUrl}" width="100%" height="100%" style="border:0;" allowfullscreen loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>`;
        }
    }

    if (navigator.geolocation && statusText) {
        statusText.textContent = 'Fetching your location...';
        navigator.geolocation.getCurrentPosition(
            (position) => {
                const lat = position.coords.latitude;
                const lng = position.coords.longitude;
                statusText.textContent = 'Live location ready';
                updateMap(lat, lng);
            },
            () => {
                statusText.textContent = 'Unable to access live location';
                if (mapBox) {
                    mapBox.innerHTML = '<div><p>Location access denied.</p><p>Enable geolocation to see your live map.</p></div>';
                }
            }
        );
    }

    const routeForm = document.getElementById('routeForm');
    const startLocationInput = document.getElementById('startLocation');
    const destinationInput = document.getElementById('destinationInput');
    const useLiveLocationBtn = document.getElementById('useLiveLocationBtn');
    const routeResetBtn = document.getElementById('routeResetBtn');
    const routeSummary = document.getElementById('routeSummary');
    const routeMapContainer = document.getElementById('routeMap');
    let routeCoords = null;

    function setRouteSummary(message, type = 'info') {
        if (routeSummary) {
            routeSummary.textContent = message;
            routeSummary.dataset.state = type;
        }
    }

    function updateRouteMap() {
        if (!routeMapContainer) return;
        if (!routeCoords) {
            routeMapContainer.innerHTML = '<div class="map-empty">Enable location access to show your safe route.</div>';
            return;
        }
        const destination = destinationInput && destinationInput.value.trim();
        if (destination) {
            setRouteSummary(`Enter a route mode above to generate the best path to ${destination}.`, 'info');
        } else {
            setRouteSummary('Destination not set yet. Enter a destination and choose SAFE or FASTEST route.', 'info');
        }
    }

    function fetchLiveRouteLocation() {
        if (!navigator.geolocation) {
            setRouteSummary('Geolocation is not supported on this browser.', 'error');
            if (routeMapContainer) {
                routeMapContainer.innerHTML = '<div class="map-empty">This browser cannot access location data.</div>';
            }
            return;
        }

        setRouteSummary('Fetching your live location...', 'info');
        navigator.geolocation.getCurrentPosition(
            (position) => {
                routeCoords = {
                    lat: position.coords.latitude,
                    lng: position.coords.longitude
                };

                if (startLocationInput) {
                    startLocationInput.value = `${routeCoords.lat.toFixed(5)}, ${routeCoords.lng.toFixed(5)}`;
                }

                updateRouteMap();
                // If a destination is already provided, render the route automatically
                if (destinationInput && destinationInput.value && destinationInput.value.trim()) {
                    try { renderRoute('safe'); } catch (e) { console.error('Auto-render route failed', e); }
                }
            },
            () => {
                setRouteSummary('Unable to access location. Enter a start point manually.', 'error');
                if (routeMapContainer) {
                    routeMapContainer.innerHTML = '<div class="map-empty">Location access denied. Enter a start point manually to continue.</div>';
                }
            }
        );
    }

    if (routeForm) {
        routeForm.addEventListener('submit', (e) => {
            e.preventDefault();
            if (!routeCoords) {
                fetchLiveRouteLocation();
            } else {
                renderRoute('safe');
            }
        });
    }

    if (useLiveLocationBtn) {
        useLiveLocationBtn.addEventListener('click', fetchLiveRouteLocation);
    }

    if (routeResetBtn) {
        routeResetBtn.addEventListener('click', () => {
            if (startLocationInput) {
                startLocationInput.value = '';
            }
            if (destinationInput) {
                destinationInput.value = '';
            }
            routeCoords = null;
            updateRouteMap();
            setRouteSummary('Reset complete. Use live location again when ready.', 'info');
        });
    }

    fetchLiveRouteLocation();

    const sosButton = document.getElementById('sosButton');
    const sosMessageInput = document.getElementById('sosMessage');
    const sosResult = document.getElementById('sosResult');
    const alertList = document.querySelector('.alert-list');

    function showSosResult(message, type = 'info') {
        if (sosResult) {
            sosResult.textContent = message;
            sosResult.className = `sos-result ${type}`;
        }
    }

    function addAlertToList(message) {
        if (!alertList) return;
        const item = document.createElement('li');
        item.className = 'alert-item';
        item.innerHTML = `
            <span>${message}</span>
            <small>${new Date().toLocaleString()}</small>
        `;
        alertList.prepend(item);
    }

    if (sosButton) {
        sosButton.addEventListener('click', async () => {
            if (!navigator.geolocation) {
                showSosResult('Geolocation is not supported by this browser.', 'error');
                return;
            }

            sosButton.disabled = true;
            sosButton.textContent = 'Sending alert...';
            showSosResult('Preparing your emergency alert...', 'info');

            navigator.geolocation.getCurrentPosition(
                async (position) => {
                    const payload = {
                        latitude: position.coords.latitude,
                        longitude: position.coords.longitude,
                        message: sosMessageInput && sosMessageInput.value.trim()
                            ? sosMessageInput.value.trim()
                            : `Emergency SOS triggered at ${new Date().toLocaleString()}`
                    };

                    try {
                        const response = await fetch('/api/sos', {
                            method: 'POST',
                            headers: { 'Content-Type': 'application/json' },
                            body: JSON.stringify(payload)
                        });

                        const data = await response.json();

                        if (!response.ok || !data.success) {
                            throw new Error(data.message || 'Unable to send alert.');
                        }

                        showSosResult(data.message || 'Alert sent successfully.', 'success');
                        addAlertToList(payload.message);

                        if (statusText) {
                            statusText.textContent = 'Alert sent successfully';
                        }
                        if (coordsText) {
                            coordsText.textContent = `${payload.latitude.toFixed(4)}, ${payload.longitude.toFixed(4)}`;
                        }
                        if (mapBox) {
                            updateMap(payload.latitude, payload.longitude);
                        }

                        const recipientContainer = document.getElementById('recipientCards');
                        if (data.recipients && Array.isArray(data.recipients) && recipientContainer) {
                            recipientContainer.innerHTML = '';
                            data.recipients.forEach((r) => {
                                const card = document.createElement('div');
                                card.className = 'panel';
                                card.style.display = 'flex';
                                card.style.justifyContent = 'space-between';
                                card.style.alignItems = 'center';
                                card.innerHTML = `
                                    <div style="display:flex;align-items:center;gap:0.6rem;">
                                        <div style="width:48px;height:48px;border-radius:50%;background:linear-gradient(135deg,var(--primary),var(--accent));color:white;display:grid;place-items:center;font-weight:800;">${(r.name || 'U').charAt(0)}</div>
                                        <div>
                                            <div style="font-weight:700">${r.name}</div>
                                            <div style="color:var(--muted)">${r.relation || ''} • ${r.phone}</div>
                                        </div>
                                    </div>
                                    <div style="text-align:right">
                                        <div style="color:var(--success);font-weight:800">✓ Sent Successfully</div>
                                        <div style="color:var(--muted);font-size:0.9rem">${new Date().toLocaleTimeString()}</div>
                                    </div>`;
                                recipientContainer.appendChild(card);
                            });
                        }
                    } catch (error) {
                        showSosResult(error.message || 'Unable to send alert.', 'error');
                    } finally {
                        sosButton.disabled = false;
                        sosButton.textContent = 'Trigger SOS';
                    }
                },
                () => {
                    showSosResult('Unable to send SOS without location access.', 'error');
                    sosButton.disabled = false;
                    sosButton.textContent = 'Trigger SOS';
                }
            );
        });
    }

    const contactForm = document.getElementById('contactForm');
    const contactList = document.getElementById('contactList');

    async function loadLearningCenter() {
        const challengeList = document.getElementById('challengeList');
        const learningList = document.getElementById('learningList');
        const xpBadge = document.getElementById('xpBadge');
        const progressBadge = document.getElementById('progressBadge');

        if (!challengeList && !learningList) return;

        const [challenges, progressRows, safetyProgress] = await Promise.all([
            fetch('/api/challenges').then((r) => r.json()),
            fetch('/api/learning-progress').then((r) => r.json()),
            fetch('/api/safety-progress').then((r) => r.json())
        ]);

        const challengeMarkup = (challenges.length ? challenges : [
            { title: 'Share live location with a trusted contact', completed: false, xp_earned: 30 },
            { title: 'Test your emergency message', completed: false, xp_earned: 25 },
            { title: 'Review your safest route plan', completed: false, xp_earned: 20 }
        ]).map((challenge) => `
            <li class="alert-item">
                <div>
                    <strong>${challenge.title}</strong>
                    <div class="muted">+${challenge.xp_earned || 0} XP</div>
                </div>
                <button class="btn-outline" data-complete="${challenge.title}">${challenge.completed ? 'Completed' : 'Start'}</button>
            </li>
        `).join('');

        challengeList.innerHTML = challengeMarkup;
        learningList.innerHTML = (progressRows.length ? progressRows : [
            { module: 'Route readiness', progress: 82, completed: false },
            { module: 'Emergency response', progress: 76, completed: false },
            { module: 'Personal safety awareness', progress: 94, completed: true }
        ]).map((item) => `
            <li class="alert-item">
                <div>
                    <strong>${item.module}</strong>
                    <div class="muted">${item.progress}% complete</div>
                </div>
                <div class="status-pill ${item.completed ? 'success' : ''}">${item.completed ? 'Done' : 'In progress'}</div>
            </li>
        `).join('');

        if (xpBadge) xpBadge.textContent = `${safetyProgress.xp || 0} XP`;
        if (progressBadge) progressBadge.textContent = `${Math.max(safetyProgress.weekly_progress || 0, safetyProgress.monthly_progress || 0)}%`;
    }

    document.addEventListener('click', async (event) => {
        const target = event.target;
        if (!(target instanceof HTMLElement)) return;
        if (target.dataset.complete) {
            const title = target.dataset.complete;
            await fetch('/api/challenges', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ title, completed: true, xp_earned: 25 })
            });
            await fetch('/api/safety-progress', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ xp: 25, level: 1, weekly_progress: 25, monthly_progress: 25 })
            });
            loadLearningCenter();
            showToast('Mission completed');
        }
    });

    if (document.getElementById('challengeList') || document.getElementById('learningList')) {
        loadLearningCenter();
    }

    async function loadContacts() {
        if (!contactList) return;
        const response = await fetch('/api/contacts');
        const contacts = await response.json();
        contactList.innerHTML = '';

        contacts.forEach((contact) => {
            const li = document.createElement('li');
            li.className = 'contact-item';
            li.innerHTML = `
                <div>
                    <strong>${contact.name}</strong><br>
                    <span>${contact.phone}</span>
                    <small>${contact.relation || ''}</small>
                </div>
                <div>
                    <button class="btn-outline" data-edit="${contact.id}">Edit</button>
                    <button class="btn-danger" data-delete="${contact.id}">Delete</button>
                </div>
            `;
            contactList.appendChild(li);
        });
    }

    if (contactForm && contactList) {
        loadContacts();

        contactForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const payload = {
                name: contactForm.name.value,
                phone: contactForm.phone.value,
                relation: contactForm.relation.value
            };

            const method = contactForm.dataset.editId ? 'PUT' : 'POST';
            const url = contactForm.dataset.editId
                ? `/api/contacts/${contactForm.dataset.editId}`
                : '/api/contacts';

            const response = await fetch(url, {
                method,
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });
            const data = await response.json();
            alert(data.message || 'Saved');
            contactForm.reset();
            delete contactForm.dataset.editId;
            loadContacts();
        });

        contactList.addEventListener('click', async (e) => {
            const target = e.target;
            if (target.dataset.delete) {
                const id = target.dataset.delete;
                const response = await fetch(`/api/contacts/${id}`, { method: 'DELETE' });
                const data = await response.json();
                alert(data.message || 'Deleted');
                loadContacts();
            } else if (target.dataset.edit) {
                const id = target.dataset.edit;
                const response = await fetch(`/api/contacts/${id}`);
                const contact = await response.json();
                if (contact && !contact.success) {
                    alert(contact.message || 'Unable to load contact.');
                    return;
                }
                if (contact) {
                    contactForm.name.value = contact.name;
                    contactForm.phone.value = contact.phone;
                    contactForm.relation.value = contact.relation || '';
                    contactForm.dataset.editId = id;
                }
            }
        });
    }

    function showToast(message) {
        const existing = document.querySelector('.toast');
        if (existing) existing.remove();
        const toast = document.createElement('div');
        toast.className = 'toast';
        toast.textContent = message;
        document.body.appendChild(toast);
        setTimeout(() => toast.remove(), 2200);
    }

    // --- Additional features: Leaflet maps, route calc, live sharing UI ---

    // Lazy-load Leaflet CSS/JS when needed
    function loadLeafletIfNeeded(callback) {
        if (window.L) {
            callback();
            return;
        }
        const css = document.createElement('link');
        css.rel = 'stylesheet';
        css.href = 'https://unpkg.com/leaflet@1.9.4/dist/leaflet.css';
        document.head.appendChild(css);

        const script = document.createElement('script');
        script.src = 'https://unpkg.com/leaflet@1.9.4/dist/leaflet.js';
        script.onload = callback;
        document.body.appendChild(script);
    }

    // Utility: format seconds to H:MM
    function formatDuration(seconds) {
        if (!seconds && seconds !== 0) return '--';
        const mins = Math.round(seconds / 60);
        if (mins < 60) return `${mins} min`;
        const hrs = Math.floor(mins / 60);
        const rem = mins % 60;
        return `${hrs}h ${rem}m`;
    }

    // ROUTE FINDER (Leaflet + OSRM)
    let routeMap, routeLayer, startMarker, destMarker;
    function initRouteMap() {
        loadLeafletIfNeeded(() => {
            if (routeMap) return;
            routeMap = L.map('routeMap', { zoomControl: false }).setView([13.0827, 80.2707], 13);
            L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                maxZoom: 19,
            }).addTo(routeMap);
            L.control.scale().addTo(routeMap);
            routeLayer = L.layerGroup().addTo(routeMap);
        });
    }

    async function computeRoute(start, dest, profile = 'driving') {
        // OSRM public server
        const url = `https://router.project-osrm.org/route/v1/${profile}/${start.lng},${start.lat};${dest.lng},${dest.lat}?overview=full&geometries=geojson&alternatives=true`;
        const res = await fetch(url);
        if (!res.ok) throw new Error('Routing service failed');
        const data = await res.json();
        return data;
    }

    async function renderRoute(choice) {
        if (!routeCoords || !destinationInput || !destinationInput.value.trim()) {
            setRouteSummary('Start or destination missing.', 'error');
            return;
        }
        initRouteMap();
        try {
            const destText = destinationInput.value.trim();
            const geocodeUrl = `https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(destText)}&limit=1`;
            const gres = await fetch(geocodeUrl, { headers: { 'Accept-Language': 'en' } });
            const gdata = await gres.json();
            if (!gdata || !gdata[0]) {
                setRouteSummary('Destination not found. Try another location.', 'error');
                return;
            }
            const dest = { lat: parseFloat(gdata[0].lat), lng: parseFloat(gdata[0].lon) };
            const start = { lat: routeCoords.lat, lng: routeCoords.lng };

            const response = await fetch('/api/route-plan', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ start, destination: dest, route_type: choice === 'safe' ? 'safest' : 'fastest' })
            });
            const routePayload = await response.json();
            if (!response.ok || !routePayload.success) throw new Error(routePayload.message || 'Unable to create route plan.');

            routeLayer.clearLayers();
            const geo = routePayload.geometry;
            const poly = L.geoJSON(geo, { style: { color: choice === 'safe' ? '#2dd4bf' : '#7c4dff', weight: 6, opacity: 0.9 } });
            poly.addTo(routeLayer);
            poly.getLayers().forEach((l) => l.setStyle({ className: 'glow-route' }));

            if (startMarker) routeLayer.removeLayer(startMarker);
            if (destMarker) routeLayer.removeLayer(destMarker);
            startMarker = L.circleMarker([start.lat, start.lng], { radius: 8, color: '#fff', weight: 2, fillColor: '#7c4dff', fillOpacity: 1 }).addTo(routeLayer);
            destMarker = L.circleMarker([dest.lat, dest.lng], { radius: 8, color: '#fff', weight: 2, fillColor: '#ef4444', fillOpacity: 1 }).addTo(routeLayer);

            routeMap.fitBounds(poly.getBounds(), { padding: [40, 40] });

            const distKm = `${routePayload.distance.toFixed(2)} km`;
            const duration = `${routePayload.duration.toFixed(1)} min`;
            const eta = new Date(Date.now() + routePayload.duration * 60 * 1000).toLocaleTimeString();
            const safetyScore = `${routePayload.risk_score} / 100`;

            document.getElementById('routeDistance').textContent = distKm;
            document.getElementById('routeDuration').textContent = duration;
            document.getElementById('routeETA').textContent = eta;
            document.getElementById('routeSafety').textContent = safetyScore;
            document.getElementById('routeInsights').innerHTML = `
                <div><strong>Route mode:</strong> ${choice === 'safe' ? 'Safer route' : 'Fastest route'}</div>
                <div><strong>Estimated risk:</strong> ${routePayload.risk_score}/100</div>
                <div><strong>Suggested action:</strong> ${routePayload.risk_score < 60 ? 'Stay on well-lit streets and notify a contact before leaving.' : 'Consider delaying the trip until you reach a safer area.'}</div>
            `;
            setRouteSummary(`Route generated (${choice.toUpperCase()}).`, 'success');

            fetch('/api/travel-history', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ route_name: choice === 'safe' ? 'Safer route' : 'Fastest route', latitude: start.lat, longitude: start.lng })
            }).catch(() => {});
        } catch (err) {
            console.error(err);
            setRouteSummary(err.message || 'Could not generate route.', 'error');
        }
    }

    if (document.getElementById('safeRouteBtn') || document.getElementById('fastRouteBtn')) {
        initRouteMap();
        document.getElementById('safeRouteBtn').addEventListener('click', () => renderRoute('safe'));
        document.getElementById('fastRouteBtn').addEventListener('click', () => renderRoute('fast'));
    }

    // LIVE SHARING
    let liveMap, liveMarker, watchId = null;
    function initLiveMap() {
        loadLeafletIfNeeded(() => {
            if (liveMap) return;
            liveMap = L.map('liveMap', { zoomControl: false }).setView([13.0827, 80.2707], 13);
            L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', { maxZoom: 19 }).addTo(liveMap);
            L.control.scale().addTo(liveMap);
        });
    }

    function updateLiveUI(pos) {
        const lat = pos.coords.latitude;
        const lng = pos.coords.longitude;
        document.getElementById('ls_lat').textContent = lat.toFixed(6);
        document.getElementById('ls_lng').textContent = lng.toFixed(6);
        document.getElementById('ls_accuracy').textContent = pos.coords.accuracy ? pos.coords.accuracy.toFixed(1) : '--';
        document.getElementById('ls_speed').textContent = pos.coords.speed != null ? pos.coords.speed.toFixed(2) : '--';
        document.getElementById('ls_heading').textContent = pos.coords.heading != null ? pos.coords.heading.toFixed(0) : '--';
        document.getElementById('ls_updated').textContent = new Date().toLocaleTimeString();
        document.getElementById('liveStatus').textContent = 'Location available';

        initLiveMap();
        if (liveMarker) liveMarker.setLatLng([lat, lng]);
        else liveMarker = L.circleMarker([lat, lng], { radius: 8, color: '#fff', weight: 2, fillColor: '#7c4dff', fillOpacity: 1 }).addTo(liveMap);
        liveMap.setView([lat, lng], liveMap.getZoom());
    }

    async function fetchShareHistory() {
        try {
            const res = await fetch('/api/share_history');
            if (!res.ok) return;
            const data = await res.json();
            const container = document.getElementById('shareHistory');
            container.innerHTML = '';
            data.forEach((s) => {
                const el = document.createElement('div');
                el.className = 'panel';
                el.style.padding = '0.6rem';
                el.innerHTML = `<div style="display:flex;justify-content:space-between;align-items:center;">
                    <div>${new Date(s.created_at).toLocaleString()} - ${parseFloat(s.latitude).toFixed(4)}, ${parseFloat(s.longitude).toFixed(4)}</div>
                    <div><a class="btn-outline" href="/shared/${s.id}">Open</a></div>
                </div>`;
                container.appendChild(el);
            });
        } catch (e) { console.error(e); }
    }

    document.addEventListener('click', async (e) => {
        if (e.target && e.target.id === 'shareLiveBtn') {
            if (!navigator.geolocation) {
                alert('Geolocation not supported');
                return;
            }
            navigator.geolocation.getCurrentPosition(async (pos) => {
                const lat = pos.coords.latitude;
                const lng = pos.coords.longitude;
                try {
                    const resp = await fetch('/api/share_live', {
                        method: 'POST', headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ latitude: lat, longitude: lng, method: 'link' })
                    });
                    const data = await resp.json();
                    if (!data.success) throw new Error(data.message || 'Unable to create share');
                    const modal = document.getElementById('shareModal');
                    const qrContainer = document.getElementById('qrContainer');
                    document.getElementById('shareInfo').textContent = data.share_url;
                    modal.style.display = 'block';
                    qrContainer.style.display = 'flex';
                    qrContainer.innerHTML = '<div class="muted">Generating QR code...</div>';

                    const qrResp = await fetch(`/api/qr?url=${encodeURIComponent(data.share_url)}`);
                    const qrData = await qrResp.json();
                    if (qrData.success) {
                        qrContainer.innerHTML = `<img src="${qrData.image}" alt="QR code" style="width:180px;height:180px;" /><div class="muted">Scan to share your live location</div>`;
                    } else {
                        qrContainer.innerHTML = '<div class="muted">QR code unavailable</div>';
                    }

                    document.getElementById('whatsappShare').onclick = () => {
                        const text = `I'm sharing my live location: ${data.share_url}`;
                        window.open(`https://wa.me/?text=${encodeURIComponent(text)}`, '_blank');
                    };
                    document.getElementById('smsShare').onclick = () => {
                        const body = `Live location: ${data.share_url}`;
                        window.location.href = `sms:?body=${encodeURIComponent(body)}`;
                    };
                    document.getElementById('emailShare').onclick = () => {
                        const subj = 'Live location shared';
                        const body = `I'm sharing my live location: ${data.share_url}`;
                        window.location.href = `mailto:?subject=${encodeURIComponent(subj)}&body=${encodeURIComponent(body)}`;
                    };
                    document.getElementById('copyLink').onclick = async () => {
                        await navigator.clipboard.writeText(data.share_url);
                        showToast('Link Copied Successfully');
                        const info = document.getElementById('shareInfo');
                        const prev = info.textContent;
                        info.textContent = 'Copied!';
                        setTimeout(() => { info.textContent = prev; }, 1400);
                    };
                    document.getElementById('nativeShare').onclick = async () => {
                        if (navigator.share) {
                            try { await navigator.share({ title: 'Live location', text: 'My live location', url: data.share_url }); }
                            catch (err) { console.warn(err); }
                        } else {
                            window.open(`https://wa.me/?text=${encodeURIComponent("Live location: " + data.share_url)}`, '_blank');
                        }
                    };

                    document.getElementById('closeShareModal').onclick = () => {
                        document.getElementById('shareModal').style.display = 'none';
                    };

                    fetchShareHistory();
                } catch (err) {
                    alert(err.message || 'Unable to share location');
                }
            }, (err) => { alert('Unable to get location'); });
        }

        if (e.target && e.target.id === 'qrShareBtn') {
            const modal = document.getElementById('shareModal');
            const qrContainer = document.getElementById('qrContainer');
            modal.style.display = 'block';
            qrContainer.style.display = 'flex';
            qrContainer.innerHTML = '<div class="muted">Use Share Live Location to generate a QR code.</div>';
        }
    });

    // stop share not yet implemented, placeholder to hide modal
    const stopBtn = document.getElementById('stopShareBtn');
    if (stopBtn) stopBtn.addEventListener('click', () => { alert('Stop sharing'); });

    // update live tracking every 5 seconds using watchPosition
    if (navigator.geolocation) {
        navigator.geolocation.watchPosition((pos) => {
            updateLiveUI(pos);
            // update route live coords used by route finder
            routeCoords = { lat: pos.coords.latitude, lng: pos.coords.longitude };
        }, (err) => { console.warn('watch error', err); }, { enableHighAccuracy: true, maximumAge: 4000, timeout: 8000 });
    }

});
