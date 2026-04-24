// ============================================================
// ODITO — Internationalisation (EN / IT / EL)
// ============================================================
const TRANSLATIONS = {
  en: {
    // Nav
    'nav.dashboard': 'Dashboard', 'nav.my_actions': 'My Actions',
    'nav.new_audit': '+ New Audit', 'nav.admin': 'Admin', 'nav.logout': 'Log Out',
    'nav.rem_report': '📊 Remediation Report',
    // Buttons
    'btn.save': 'Save', 'btn.save_changes': 'Save Changes', 'btn.cancel': 'Cancel',
    'btn.create': 'Create', 'btn.create_report': 'Create Report', 'btn.edit': '✏ Edit',
    'btn.delete': 'Delete', 'btn.send': 'Send', 'btn.add': '+ Add', 'btn.close': 'Close',
    'btn.sign_in': 'Sign In', 'btn.create_account': 'Create Account',
    'btn.new_user': '+ New User', 'btn.role': 'Role', 'btn.extract': '🚀 Extract',
    'btn.log': 'Log', 'btn.update_status': 'Update status:',
    // Status
    'status.pending': 'Pending', 'status.in_progress': 'In Progress',
    'status.completed': 'Completed', 'status.overdue': 'Overdue',
    'status.open': 'Open', 'status.closed': 'Closed',
    // Priority
    'priority.1': 'High', 'priority.2': 'Relevant', 'priority.3': 'Medium', 'priority.4': 'Low',
    // Results
    'result.Good': 'Good', 'result.Satisfactory': 'Satisfactory',
    'result.Unsatisfactory': 'Unsatisfactory', 'result.Poor': 'Poor',
    // Form labels — audit
    'label.report_ref': 'Report Code *', 'label.title': 'Title *',
    'label.audited_entity': 'Audited Entity', 'label.audit_type': 'Audit Type',
    'label.audit_class': 'Audit Class', 'label.overall_result': 'Overall Result',
    'label.previous_result': 'Previous Result', 'label.previous_result_date': 'Previous Result Date',
    'label.issue_date': 'Issue Date', 'label.sample_from': 'Sample Period — From',
    'label.sample_to': 'Sample Period — To', 'label.field_from': 'Fieldwork Period — From',
    'label.field_to': 'Fieldwork Period — To', 'label.cae': 'Chief Audit Executive',
    'label.team_manager': 'Audit Team Manager', 'label.team': 'Audit Team',
    'label.exit_date': 'Exit Meeting Date', 'label.exit_participants': 'Exit Meeting Participants',
    'label.background': 'Background / Scope',
    // Form labels — finding
    'label.finding_ref': 'Number / Ref *', 'label.priority': 'Priority *',
    'label.description': 'Description', 'label.article_ref': 'Regulatory Reference',
    'label.root_cause': 'Root Cause', 'label.recommendation': 'Recommendation',
    // Form labels — measure
    'label.deadline': 'Deadline *', 'label.owner': 'Owner (user)',
    'label.owner_name': 'Owner Name (free text)', 'label.status': 'Status', 'label.notes': 'Notes',
    // Form labels — admin
    'label.full_name': 'Full name *', 'label.email': 'Email', 'label.password': 'Password',
    'label.new_password': 'New password *', 'label.new_role': 'New role',
    // Section titles
    'section.report_header': 'Report Header', 'section.periods': 'Periods',
    'section.audit_team': 'Audit Team', 'section.background': 'Background / Scope',
    'section.findings': 'Non-Conformities', 'section.measures': 'Corrective Measures',
    'section.log': 'Remediation Log', 'section.users': 'User Management',
    // Page headings
    'page.new_audit': 'New Audit Report', 'page.new_audit_sub': 'Import from PDF or fill manually',
    'page.my_actions': 'My Actions', 'page.admin': 'Administration Panel',
    'page.admin_sub': 'User management and system configuration',
    // Dashboard
    'stat.total_audits': 'Total Audits', 'stat.open_audits': 'Open Audits',
    'stat.open_findings': 'Open Non-Conformities', 'stat.overdue': 'Overdue Measures',
    'stat.completed': 'Completed Measures', 'stat.recent_audits': 'Recent Audits',
    'stat.by_priority': 'Non-Conformities by Priority', 'stat.deadlines': 'Upcoming Deadlines',
    // Messages
    'msg.loading': 'Loading...', 'msg.no_audits': 'No audits yet',
    'msg.no_findings': 'No non-conformities recorded', 'msg.no_measures': 'No corrective measures',
    'msg.no_actions': 'No actions found', 'msg.no_deadlines': 'No upcoming deadlines',
    'msg.no_logs': 'No notes yet', 'msg.select_measure': 'Select a measure to view the remediation log',
    'msg.findings': 'findings', 'msg.measures_done': 'completed',
    // Login / Register
    'login.title': 'Sign in to your account', 'login.no_account': "Don't have an account?",
    'login.register_link': 'Register',
    'register.title': 'Create your account', 'register.name': 'Full name',
    'register.have_account': 'Already have an account?', 'register.login_link': 'Sign In',
    // Admin table
    'admin.col.name': 'Name', 'admin.col.email': 'Email', 'admin.col.role': 'Role',
    'admin.col.registered': 'Registered', 'admin.col.actions': 'Actions',
    'admin.stat.users': 'Total Users', 'admin.stat.auditors': 'Auditors',
    'admin.stat.operational': 'Operational', 'admin.stat.admins': 'Admins',
    'admin.modal.create': 'Create new user', 'admin.modal.role': 'Change role',
    'admin.modal.pwd': 'Reset password',
    'admin.confirm_delete': 'Delete user "%s"? This cannot be undone.',
    // Roles
    'role.admin': 'Admin', 'role.auditor': 'Auditor', 'role.operational': 'Operational',
    // Tabs
    'tab.findings': 'Non-Conformities', 'tab.edit': 'Edit Report',
    // Finding detail
    'finding.reg_ref': 'Regulatory reference', 'finding.root_cause': 'Root Cause',
    'finding.recommendation': 'Recommendation',
    // Filters
    'filter.status': 'Status:', 'filter.priority': 'Priority:',
    'filter.all_status': 'All', 'filter.all_priority': 'All',
    // PDF import
    'pdf.title': '🤖 Import from PDF with AI',
    'pdf.drop': 'Drop PDF here or', 'pdf.drop_link': 'click to select',
    'pdf.hint': 'ChatGPT will automatically extract all fields and non-conformities',
    'pdf.extracting': 'Extracting with ChatGPT...', 'pdf.success': 'Extraction complete —',
    'pdf.found': 'non-conformities found',
    'pdf.truncated': '(PDF truncated, some data may be missing)',
    'pdf.key_placeholder': 'OpenAI API key (sk-...)',
    'pdf.key_hint': 'The key is not saved on the server.',
    'pdf.extracted': 'Extracted non-conformities',
    'pdf.auto_create': 'Will be created automatically on save',
    // Select options
    'select.choose': '— select —',
    // Errors
    'err.ref_title': 'Report Code and Title are required',
    'err.ref_priority_title': 'Number, priority and title are required',
    'err.desc_deadline': 'Description and deadline are required',
    'err.enter_note': 'Please enter a note',
    'err.all_fields': 'Please fill all fields',
    // Greeting
    'greeting': 'Welcome',
    // Misc
    'misc.findings_count': 'findings',
    'misc.not_found': 'Audit not found',
    'misc.finding_not_found': 'Non-conformity not found',
    'misc.cancel': 'Cancel',
  },

  it: {
    'nav.dashboard': 'Dashboard', 'nav.my_actions': 'Le mie azioni',
    'nav.new_audit': '+ Nuovo Audit', 'nav.admin': 'Admin', 'nav.logout': 'Esci',
    'nav.rem_report': '📊 Report Remediation',
    'btn.save': 'Salva', 'btn.save_changes': 'Salva modifiche', 'btn.cancel': 'Annulla',
    'btn.create': 'Crea', 'btn.create_report': 'Crea Report', 'btn.edit': '✏ Modifica',
    'btn.delete': 'Elimina', 'btn.send': 'Invia', 'btn.add': '+ Aggiungi', 'btn.close': 'Chiudi',
    'btn.sign_in': 'Accedi', 'btn.create_account': 'Registrati',
    'btn.new_user': '+ Nuovo utente', 'btn.role': 'Ruolo', 'btn.extract': '🚀 Estrai',
    'btn.log': 'Log', 'btn.update_status': 'Aggiorna stato:',
    'status.pending': 'In attesa', 'status.in_progress': 'In corso',
    'status.completed': 'Completato', 'status.overdue': 'Scaduto',
    'status.open': 'Aperta', 'status.closed': 'Chiusa',
    'priority.1': 'Alta', 'priority.2': 'Rilevante', 'priority.3': 'Media', 'priority.4': 'Bassa',
    'result.Good': 'Good', 'result.Satisfactory': 'Satisfactory',
    'result.Unsatisfactory': 'Unsatisfactory', 'result.Poor': 'Poor',
    'label.report_ref': 'Codice Report *', 'label.title': 'Titolo *',
    'label.audited_entity': 'Entità Auditata', 'label.audit_type': 'Tipo Audit',
    'label.audit_class': 'Classe Audit', 'label.overall_result': 'Risultato Complessivo',
    'label.previous_result': 'Risultato Precedente', 'label.previous_result_date': 'Data Risultato Precedente',
    'label.issue_date': 'Data Emissione', 'label.sample_from': 'Periodo Campione — Da',
    'label.sample_to': 'Periodo Campione — A', 'label.field_from': 'Periodo Fieldwork — Da',
    'label.field_to': 'Periodo Fieldwork — A', 'label.cae': 'Chief Audit Executive',
    'label.team_manager': 'Audit Team Manager', 'label.team': 'Audit Team',
    'label.exit_date': 'Data Exit Meeting', 'label.exit_participants': 'Partecipanti Exit Meeting',
    'label.background': 'Background / Scope',
    'label.finding_ref': 'Numero / Ref *', 'label.priority': 'Priorità *',
    'label.description': 'Descrizione', 'label.article_ref': 'Riferimento Normativo',
    'label.root_cause': 'Root Cause', 'label.recommendation': 'Raccomandazione',
    'label.deadline': 'Scadenza *', 'label.owner': 'Responsabile (utente)',
    'label.owner_name': 'Nome Responsabile (libero)', 'label.status': 'Stato', 'label.notes': 'Note',
    'label.full_name': 'Nome completo *', 'label.email': 'Email', 'label.password': 'Password',
    'label.new_password': 'Nuova password *', 'label.new_role': 'Nuovo ruolo',
    'section.report_header': 'Intestazione Report', 'section.periods': 'Periodi',
    'section.audit_team': 'Team di Audit', 'section.background': 'Background / Scope',
    'section.findings': 'Non Conformità', 'section.measures': 'Misure Correttive',
    'section.log': 'Log Remediation', 'section.users': 'Gestione Utenti',
    'page.new_audit': 'Nuovo Audit Report', 'page.new_audit_sub': 'Importa da PDF oppure compila manualmente',
    'page.my_actions': 'Le mie azioni', 'page.admin': 'Pannello Amministrazione',
    'page.admin_sub': 'Gestione utenti e configurazione sistema',
    'stat.total_audits': 'Audit totali', 'stat.open_audits': 'Audit aperti',
    'stat.open_findings': 'Non conformità aperte', 'stat.overdue': 'Misure scadute',
    'stat.completed': 'Misure completate', 'stat.recent_audits': 'Audit recenti',
    'stat.by_priority': 'Non conformità per priorità', 'stat.deadlines': 'Prossime scadenze',
    'msg.loading': 'Caricamento...', 'msg.no_audits': 'Nessun audit ancora',
    'msg.no_findings': 'Nessuna non conformità registrata', 'msg.no_measures': 'Nessuna misura correttiva',
    'msg.no_actions': 'Nessuna azione trovata', 'msg.no_deadlines': 'Nessuna scadenza imminente',
    'msg.no_logs': 'Nessuna nota ancora', 'msg.select_measure': 'Seleziona una misura per vedere il log di remediation',
    'msg.findings': 'finding', 'msg.measures_done': 'completate',
    'login.title': 'Accedi al tuo account', 'login.no_account': 'Non hai un account?',
    'login.register_link': 'Registrati',
    'register.title': 'Crea il tuo account', 'register.name': 'Nome completo',
    'register.have_account': 'Hai già un account?', 'register.login_link': 'Accedi',
    'admin.col.name': 'Nome', 'admin.col.email': 'Email', 'admin.col.role': 'Ruolo',
    'admin.col.registered': 'Registrato', 'admin.col.actions': 'Azioni',
    'admin.stat.users': 'Utenti totali', 'admin.stat.auditors': 'Auditor',
    'admin.stat.operational': 'Operativi', 'admin.stat.admins': 'Admin',
    'admin.modal.create': 'Crea nuovo utente', 'admin.modal.role': 'Cambia ruolo',
    'admin.modal.pwd': 'Reset password',
    'admin.confirm_delete': 'Eliminare l\'utente "%s"? L\'operazione non può essere annullata.',
    'role.admin': 'Admin', 'role.auditor': 'Auditor', 'role.operational': 'Operativo',
    'tab.findings': 'Non Conformità', 'tab.edit': 'Modifica Report',
    'finding.reg_ref': 'Riferimento normativo', 'finding.root_cause': 'Root Cause',
    'finding.recommendation': 'Raccomandazione',
    'filter.status': 'Stato:', 'filter.priority': 'Priorità:',
    'filter.all_status': 'Tutti', 'filter.all_priority': 'Tutte',
    'pdf.title': '🤖 Importa da PDF con AI',
    'pdf.drop': 'Trascina il PDF qui oppure', 'pdf.drop_link': 'clicca per selezionare',
    'pdf.hint': 'ChatGPT estrarrà automaticamente tutti i campi e le non conformità',
    'pdf.extracting': 'Estrazione in corso con ChatGPT...', 'pdf.success': 'Estrazione completata —',
    'pdf.found': 'non conformità trovate',
    'pdf.truncated': '(PDF troncato, alcuni dati potrebbero mancare)',
    'pdf.key_placeholder': 'OpenAI API key (sk-...)',
    'pdf.key_hint': 'La chiave non viene salvata sul server.',
    'pdf.extracted': 'Non conformità estratte',
    'pdf.auto_create': 'Verranno create automaticamente al salvataggio',
    'select.choose': '— seleziona —',
    'err.ref_title': 'Codice Report e Titolo sono obbligatori',
    'err.ref_priority_title': 'Numero, priorità e titolo obbligatori',
    'err.desc_deadline': 'Descrizione e scadenza obbligatorie',
    'err.enter_note': 'Inserisci una nota',
    'err.all_fields': 'Compila tutti i campi',
    'greeting': 'Benvenuto',
    'misc.findings_count': 'finding',
    'misc.not_found': 'Audit non trovato',
    'misc.finding_not_found': 'Non conformità non trovata',
    'misc.cancel': 'Annulla',
  },

  el: {
    'nav.dashboard': 'Πίνακας', 'nav.my_actions': 'Οι ενέργειές μου',
    'nav.new_audit': '+ Νέος Έλεγχος', 'nav.admin': 'Διαχείριση', 'nav.logout': 'Αποσύνδεση',
    'nav.rem_report': '📊 Αναφορά Αποκατάστασης',
    'btn.save': 'Αποθήκευση', 'btn.save_changes': 'Αποθήκευση αλλαγών', 'btn.cancel': 'Ακύρωση',
    'btn.create': 'Δημιουργία', 'btn.create_report': 'Δημιουργία Αναφοράς', 'btn.edit': '✏ Επεξεργασία',
    'btn.delete': 'Διαγραφή', 'btn.send': 'Αποστολή', 'btn.add': '+ Προσθήκη', 'btn.close': 'Κλείσιμο',
    'btn.sign_in': 'Σύνδεση', 'btn.create_account': 'Δημιουργία λογαριασμού',
    'btn.new_user': '+ Νέος χρήστης', 'btn.role': 'Ρόλος', 'btn.extract': '🚀 Εξαγωγή',
    'btn.log': 'Αρχείο', 'btn.update_status': 'Ενημέρωση κατάστασης:',
    'status.pending': 'Σε αναμονή', 'status.in_progress': 'Σε εξέλιξη',
    'status.completed': 'Ολοκληρώθηκε', 'status.overdue': 'Εκπρόθεσμο',
    'status.open': 'Ανοιχτή', 'status.closed': 'Κλειστή',
    'priority.1': 'Υψηλή', 'priority.2': 'Σημαντική', 'priority.3': 'Μέτρια', 'priority.4': 'Χαμηλή',
    'result.Good': 'Good', 'result.Satisfactory': 'Satisfactory',
    'result.Unsatisfactory': 'Unsatisfactory', 'result.Poor': 'Poor',
    'label.report_ref': 'Κωδικός Αναφοράς *', 'label.title': 'Τίτλος *',
    'label.audited_entity': 'Ελεγχόμενη Οντότητα', 'label.audit_type': 'Τύπος Ελέγχου',
    'label.audit_class': 'Κατηγορία Ελέγχου', 'label.overall_result': 'Συνολικό Αποτέλεσμα',
    'label.previous_result': 'Προηγούμενο Αποτέλεσμα', 'label.previous_result_date': 'Ημερομηνία Προηγούμενου',
    'label.issue_date': 'Ημερομηνία Έκδοσης', 'label.sample_from': 'Περίοδος Δείγματος — Από',
    'label.sample_to': 'Περίοδος Δείγματος — Έως', 'label.field_from': 'Επιτόπιος Έλεγχος — Από',
    'label.field_to': 'Επιτόπιος Έλεγχος — Έως', 'label.cae': 'Επικεφαλής Εσωτερικού Ελέγχου',
    'label.team_manager': 'Διαχειριστής Ομάδας', 'label.team': 'Ομάδα Ελέγχου',
    'label.exit_date': 'Ημ. Τελικής Συνάντησης', 'label.exit_participants': 'Συμμετέχοντες Τελικής Συνάντησης',
    'label.background': 'Ιστορικό / Πεδίο Εφαρμογής',
    'label.finding_ref': 'Αριθμός / Αναφορά *', 'label.priority': 'Προτεραιότητα *',
    'label.description': 'Περιγραφή', 'label.article_ref': 'Κανονιστική Αναφορά',
    'label.root_cause': 'Βασική Αιτία', 'label.recommendation': 'Σύσταση',
    'label.deadline': 'Προθεσμία *', 'label.owner': 'Υπεύθυνος (χρήστης)',
    'label.owner_name': 'Όνομα Υπεύθυνου (ελεύθερο)', 'label.status': 'Κατάσταση', 'label.notes': 'Σημειώσεις',
    'label.full_name': 'Ονοματεπώνυμο *', 'label.email': 'Email', 'label.password': 'Κωδικός',
    'label.new_password': 'Νέος κωδικός *', 'label.new_role': 'Νέος ρόλος',
    'section.report_header': 'Κεφαλίδα Αναφοράς', 'section.periods': 'Περίοδοι',
    'section.audit_team': 'Ομάδα Ελέγχου', 'section.background': 'Ιστορικό / Πεδίο',
    'section.findings': 'Μη Συμμορφώσεις', 'section.measures': 'Διορθωτικά Μέτρα',
    'section.log': 'Αρχείο Αποκατάστασης', 'section.users': 'Διαχείριση Χρηστών',
    'page.new_audit': 'Νέα Αναφορά Ελέγχου', 'page.new_audit_sub': 'Εισαγωγή από PDF ή χειροκίνητη συμπλήρωση',
    'page.my_actions': 'Οι ενέργειές μου', 'page.admin': 'Πίνακας Διαχείρισης',
    'page.admin_sub': 'Διαχείριση χρηστών και διαμόρφωση συστήματος',
    'stat.total_audits': 'Σύνολο Ελέγχων', 'stat.open_audits': 'Ανοιχτοί Έλεγχοι',
    'stat.open_findings': 'Ανοιχτές Μη Συμμορφώσεις', 'stat.overdue': 'Εκπρόθεσμα Μέτρα',
    'stat.completed': 'Ολοκληρωμένα Μέτρα', 'stat.recent_audits': 'Πρόσφατοι Έλεγχοι',
    'stat.by_priority': 'Μη Συμμορφώσεις ανά Προτεραιότητα', 'stat.deadlines': 'Επερχόμενες Προθεσμίες',
    'msg.loading': 'Φόρτωση...', 'msg.no_audits': 'Δεν υπάρχουν ακόμη έλεγχοι',
    'msg.no_findings': 'Δεν έχουν καταγραφεί μη συμμορφώσεις', 'msg.no_measures': 'Δεν υπάρχουν διορθωτικά μέτρα',
    'msg.no_actions': 'Δεν βρέθηκαν ενέργειες', 'msg.no_deadlines': 'Δεν υπάρχουν επερχόμενες προθεσμίες',
    'msg.no_logs': 'Δεν υπάρχουν σημειώσεις', 'msg.select_measure': 'Επιλέξτε ένα μέτρο για το αρχείο αποκατάστασης',
    'msg.findings': 'ευρήματα', 'msg.measures_done': 'ολοκληρωμένα',
    'login.title': 'Σύνδεση στον λογαριασμό σας', 'login.no_account': 'Δεν έχετε λογαριασμό;',
    'login.register_link': 'Εγγραφή',
    'register.title': 'Δημιουργία λογαριασμού', 'register.name': 'Ονοματεπώνυμο',
    'register.have_account': 'Έχετε ήδη λογαριασμό;', 'register.login_link': 'Σύνδεση',
    'admin.col.name': 'Όνομα', 'admin.col.email': 'Email', 'admin.col.role': 'Ρόλος',
    'admin.col.registered': 'Εγγραφή', 'admin.col.actions': 'Ενέργειες',
    'admin.stat.users': 'Σύνολο Χρηστών', 'admin.stat.auditors': 'Ελεγκτές',
    'admin.stat.operational': 'Επιχειρησιακοί', 'admin.stat.admins': 'Διαχειριστές',
    'admin.modal.create': 'Δημιουργία νέου χρήστη', 'admin.modal.role': 'Αλλαγή ρόλου',
    'admin.modal.pwd': 'Επαναφορά κωδικού',
    'admin.confirm_delete': 'Διαγραφή χρήστη "%s"; Η ενέργεια δεν μπορεί να αναιρεθεί.',
    'role.admin': 'Διαχειριστής', 'role.auditor': 'Ελεγκτής', 'role.operational': 'Επιχειρησιακός',
    'tab.findings': 'Μη Συμμορφώσεις', 'tab.edit': 'Επεξεργασία Αναφοράς',
    'finding.reg_ref': 'Κανονιστική αναφορά', 'finding.root_cause': 'Βασική Αιτία',
    'finding.recommendation': 'Σύσταση',
    'filter.status': 'Κατάσταση:', 'filter.priority': 'Προτεραιότητα:',
    'filter.all_status': 'Όλες', 'filter.all_priority': 'Όλες',
    'pdf.title': '🤖 Εισαγωγή από PDF με AI',
    'pdf.drop': 'Σύρετε το PDF εδώ ή', 'pdf.drop_link': 'κάντε κλικ για επιλογή',
    'pdf.hint': 'Το ChatGPT θα εξάγει αυτόματα όλα τα πεδία και τις μη συμμορφώσεις',
    'pdf.extracting': 'Εξαγωγή με ChatGPT...', 'pdf.success': 'Η εξαγωγή ολοκληρώθηκε —',
    'pdf.found': 'μη συμμορφώσεις βρέθηκαν',
    'pdf.truncated': '(PDF περικόπηκε, ορισμένα δεδομένα ενδέχεται να λείπουν)',
    'pdf.key_placeholder': 'OpenAI API key (sk-...)',
    'pdf.key_hint': 'Το κλειδί δεν αποθηκεύεται στον διακομιστή.',
    'pdf.extracted': 'Εξαγόμενες μη συμμορφώσεις',
    'pdf.auto_create': 'Θα δημιουργηθούν αυτόματα κατά την αποθήκευση',
    'select.choose': '— επιλέξτε —',
    'err.ref_title': 'Ο κωδικός αναφοράς και ο τίτλος είναι υποχρεωτικοί',
    'err.ref_priority_title': 'Αριθμός, προτεραιότητα και τίτλος είναι υποχρεωτικά',
    'err.desc_deadline': 'Η περιγραφή και η προθεσμία είναι υποχρεωτικές',
    'err.enter_note': 'Εισάγετε μια σημείωση',
    'err.all_fields': 'Συμπληρώστε όλα τα πεδία',
    'greeting': 'Καλώς ήρθατε',
    'misc.findings_count': 'ευρήματα',
    'misc.not_found': 'Ο έλεγχος δεν βρέθηκε',
    'misc.finding_not_found': 'Η μη συμμόρφωση δεν βρέθηκε',
    'misc.cancel': 'Ακύρωση',
  }
};

// ── Inject lang-switcher CSS once ───────────────────────────
(function(){
  const s=document.createElement('style');
  s.textContent=`.lang-switcher{display:flex;gap:.2rem}.lang-btn{background:none;border:1px solid var(--border);color:var(--text2);padding:.25rem .5rem;border-radius:5px;cursor:pointer;font-size:.75rem;font-weight:700;transition:all .15s}.lang-btn:hover{background:var(--surface2)}.lang-btn.active{background:var(--accent);color:#fff;border-color:var(--accent)}`;
  document.head.appendChild(s);
})();

// ── Core functions ───────────────────────────────────────────
let _lang = localStorage.getItem('odito-lang') || 'en';

function t(key, ...args) {
  const str = (TRANSLATIONS[_lang] || TRANSLATIONS['en'])[key]
           || (TRANSLATIONS['en'])[key]
           || key;
  // Simple %s substitution
  return str.replace(/%s/g, () => args.shift() || '');
}

function setLang(lang) {
  _lang = lang;
  localStorage.setItem('odito-lang', lang);
  applyTranslations();
  // Re-render dynamic content if a page-level render function exists
  if (typeof renderPage === 'function') renderPage();
}

function applyTranslations() {
  // Text content
  document.querySelectorAll('[data-i18n]').forEach(el => {
    el.textContent = t(el.dataset.i18n);
  });
  // Placeholders
  document.querySelectorAll('[data-i18n-ph]').forEach(el => {
    el.placeholder = t(el.dataset.i18nPh);
  });
  // Update lang button active state
  document.querySelectorAll('.lang-btn').forEach(btn => {
    btn.classList.toggle('active', btn.dataset.lang === _lang);
  });
}

// ── Nav language switcher HTML snippet ───────────────────────
// Call this to inject the switcher into any nav element
function injectLangSwitcher(navEl) {
  const div = document.createElement('div');
  div.className = 'lang-switcher';
  div.innerHTML = ['en','it','el'].map(l =>
    `<button class="lang-btn${_lang===l?' active':''}" data-lang="${l}" onclick="setLang('${l}')">${l.toUpperCase()}</button>`
  ).join('');
  navEl.appendChild(div);
}

// Shared nav user display helper
function setNavUser(me) {
  const roleKey = me.is_admin ? 'role.admin' : `role.${me.role}`;
  const roleLabel = t(roleKey);
  const el = document.getElementById('navUser');
  if (el) el.textContent = `${me.name} (${roleLabel}) — ${t('nav.logout')}`;
}

// Shared nav links i18n
function applyNavLinks() {
  const map = {
    navDashboard: 'nav.dashboard',
    navActions:   'nav.my_actions',
    navNewAudit:  'nav.new_audit',
    navRemReport: 'nav.rem_report',
    navAdmin:     'nav.admin',
  };
  Object.entries(map).forEach(([id, key]) => {
    const el = document.getElementById(id);
    if (el) el.textContent = t(key);
  });
}
