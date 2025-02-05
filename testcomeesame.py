def quiz():
    score = 0

    print("Benvenuto al quiz sui Sistemi Operativi!\n")

    # Domanda 1
    print("Domanda 1:")
    print("In un hard disk da 512 Gigabyte, per scrivere il numero di un blocco vengono usati 27 bit, arrotondati al minimo numero di byte necessario. L'hard disk adotta una allocazione indicizzata semplice, e di un file A si sa che nel suo blocco indice 20 byte vengono usati per tenere traccia dei blocchi di dati di A. Quanto può essere grande al massimo A?")
    print("a. 20 Kilobyte")
    print("b. 24 Kilobyte")
    print("c. 18 Kilobyte")
    print("d. 16 Kilobyte")
    answer1 = input("La tua risposta (a/b/c/d): ").strip().lower()
    if answer1 == "a":
        print("Corretto!\n")
        score += 1
    else:
        print("Sbagliato! La risposta corretta è: a. 20 Kilobyte\n")

    # Domanda 2
    print("Domanda 2:")
    print("Dopo l'esecuzione dei seguenti comandi in un ambiente Unix:")
    print("1. cd /tmp")
    print("2. mkdir newfolder")
    print("3. cd newfolder")
    print("4. echo 'ciao' > pippo")
    print("5. ln pippo paperino")
    print("6. ln -s /tmp/newfolder folder2")
    print("7. cp paperino topolino")
    print("8. echo 'salve' >> topolino")
    print("9. rm pippo")
    print("10. cat paperino")
    print("11. mkdir ../folder3")
    print("Quale delle seguenti affermazioni è corretta?")
    print("a. 1. Il link-counter dell'i-node di paperino è: 1")
    print("   2. Il link counter di newfolder è: 2")
    print("   3. L'output del comando 10 è: 'ciao'")
    print("   4. Il link counter di tmp è: aumentato di 3")
    print("b. 1. Il link-counter dell'i-node di paperino è: 2")
    print("   2. Il link counter di newfolder è: 2")
    print("   3. L'output del comando 10 è: 'ciao'")
    print("   4. Il link counter di tmp è: aumentato di 3")
    print("c. 1. Il link-counter dell'i-node di paperino è: 2")
    print("   2. Il link counter di newfolder è: 2")
    print("   3. L'output del comando 10 è: 'ciao'")
    print("   4. Il link counter di tmp è: aumentato di 1")
    print("d. 1. Il link-counter dell'i-node di paperino è: 1")
    print("   2. Il link counter di newfolder è: 2")
    print("   3. L'output del comando 10 è: 'ciao'")
    print("   4. Il link counter di tmp è: aumentato di 2")
    answer2 = input("La tua risposta (a/b/c/d): ").strip().lower()
    if answer2 == "d":
        print("Corretto!\n")
        score += 1
    else:
        print("Sbagliato! La risposta corretta è: d\n")

    # Domanda 3
    print("Domanda 3:")
    print("Le caratteristiche fondamentali dell'algoritmo di scheduling RR (Round Robin) sono:")
    print("a. 1. Al diminuire del quanto di tempo aumenta l'overhead dei context switch")
    print("   2. Fornisce mediamente waiting time migliori di quelli di SJF")
    print("   3. All'aumentare del quanto di tempo tende a comportarsi come FCFS")
    print("   4. È l'algoritmo di base naturale dei sistemi time sharing")
    print("b. 1. All'aumentare del quanto di tempo tende a comportarsi come FCFS")
    print("   2. È l'algoritmo di base naturale dei sistemi time sharing")
    print("   3. Al diminuire del quanto di tempo diminuisce l'overhead dei context switch")
    print("   4. Fornisce mediamente un buon tempo di risposta")
    print("c. 1. Al diminuire del quanto di tempo aumenta l'overhead dei context switch")
    print("   2. Fornisce mediamente un buon tempo di risposta")
    print("   3. Al diminuire del quanto di tempo tende a comportarsi come FCFS")
    print("   4. È l'algoritmo di base naturale dei sistemi time sharing")
    print("d. 1. Fornisce mediamente un buon tempo di risposta")
    print("   2. È l'algoritmo di base naturale dei sistemi time sharing")
    print("   3. Al diminuire del quanto di tempo aumenta l'overhead dei context switch")
    print("   4. All'aumentare del quanto di tempo tende a comportarsi come FCFS")
    answer3 = input("La tua risposta (a/b/c/d): ").strip().lower()
    if answer3 == "d":
        print("Corretto!\n")
        score += 1
    else:
        print("Sbagliato! La risposta corretta è: d\n")

    # Domanda 4
    print("Domanda 4:")
    print("Tra le ragioni per cui un sistema operativo può finire in una condizione di thrashing troviamo:")
    print("a. Un elevato numero di processi attivi rispetto alla dimensione della memoria principale, e l'adozione di un algoritmo di sostituzione delle pagine di tipo FIFO")
    print("b. Un elevato numero di processi attivi rispetto alla dimensione della memoria principale, e l'adozione di una politica di allocazione globale o locale dei frame")
    print("c. Un elevato numero di processi I/O bound rispetto alla dimensione della memoria principale, e l'adozione di una politica di allocazione globale o locale dei frame")
    print("d. Un elevato numero di processi CPU bound rispetto alla dimensione della memoria principale, e l'adozione di una politica di allocazione globale o locale dei frame")
    answer4 = input("La tua risposta (a/b/c/d): ").strip().lower()
    if answer4 == "b":
        print("Corretto!\n")
        score += 1
    else:
        print("Sbagliato! La risposta corretta è: b\n")

    # Domanda 5
    print("Domanda 5:")
    print("Dire che un sistema adotta un binding dinamico degli indirizzi significa che:")
    print("a. I programmi che girano su quel sistema usano solo indirizzi relativi, che vengono tradotti in indirizzi assoluti durante l’esecuzione delle istruzioni che usano quegli indirizzi")
    print("b. Il sistema operativo traduce gli indirizzi usati dai processi in esecuzione in modo dinamico, ossia solo nel momento in cui tali processi stanno per passare dallo stato 'ready to run' allo stato 'running'")
    print("c. I programmi che girano su quel sistema usano solo la memoria dinamica per allocare le variabili, ottimizzando così lo spazio occupato da ciascun programma")
    print("d. Gli indirizzi relativi usati dalle istruzioni dei programmi in esecuzione possono cambiare da una esecuzione alla successiva")
    answer5 = input("La tua risposta (a/b/c/d): ").strip().lower()
    if answer5 == "a":
        print("Corretto!\n")
        score += 1
    else:
        print("Sbagliato! La risposta corretta è: a\n")

    # Domanda 6
    print("Domanda 6:")
    print("Di un sistema è noto che la tabella delle pagine più grande del sistema occupa esattamente 4 frame, il numero di un frame è scritto su 4 byte usando solo i primi 26 bit, e nel sistema sono presenti in media 4 processi che insieme producono una frammentazione interna complessiva media di 2 Kilobyte.")
    print("Lo spazio logico del sistema è grande:")
    print("a. 1 Megabyte")
    print("b. 64 Gigabyte")
    print("c. 32 Gigabyte")
    print("d. 16 Gigabyte")
    answer6 = input("La tua risposta (a/b/c/d): ").strip().lower()
    if answer6 == "a":
        print("Corretto!\n")
        score += 1
    else:
        print("Sbagliato! La risposta corretta è: a. 1 Megabyte\n")

    # Domanda 7
    print("Domanda 7:")
    print("Su un hard disk che adotta una allocazione concatenata (senza FAT) è memorizzato un file A della dimensione di 0x4000 byte, e si sa che nell'ultimo blocco di A sono presenti 16 byte del file. Si sa inoltre che per scrivere il numero di un blocco vengono usati 27 bit, arrotondati al minimo numero di byte necessario. Quanto è grosso l'hard disk?")
    print("a. 128 Gigabyte")
    print("b. 1 Terabyte")
    print("c. 512 Gigabyte")
    print("d. 256 Gigabyte")
    answer7 = input("La tua risposta (a/b/c/d): ").strip().lower()
    if answer7 == "c":
        print("Corretto!\n")
        score += 1
    else:
        print("Sbagliato! La risposta corretta è: c. 512 Gigabyte\n")

    # Domanda 8
    print("Domanda 8:")
    print("Assumendo che siano presenti in un sistema almeno due processi utente, quattro possibili ragioni per cui in un moderno sistema operativo time sharing che implementa la memoria virtuale si può verificare un context switch tra due processi utente sono:")
    print("a. 1. Il processo running esegue una wait e si addormenta sul semaforo")
    print("   2. Il processo running genera page fault")
    print("   3. Il processo running genera una trap e viene terminato")
    print("   4. Il processo running inizia una operazione di I/O")
    print("b. 1. Il processo running esegue una wait e si addormenta sul semaforo")
    print("   2. Il processo running genera page fault")
    print("   3. Il processo running genera una trap e viene terminato")
    print("   4. Il processo in coda di ready inizia una operazione di I/O")
    print("c. 1. Il processo running esegue una wait e si addormenta sul semaforo")
    print("   2. Il processo running genera page fault")
    print("   3. Il processo running genera una trap e viene terminato")
    print("   4. Il processo running inizia una operazione di I/O")
    print("d. 1. Il processo running esegue una signal e si addormenta sul semaforo")
    print("   2. Il processo running genera page fault")
    print("   3. Il processo running genera una trap e viene terminato")
    print("   4. Il processo running inizia una operazione di I/O")
    answer8 = input("La tua risposta (a/b/c/d): ").strip().lower()
    if answer8 == "c":
        print("Corretto!\n")
        score += 1
    else:
        print("Sbagliato! La risposta corretta è: c\n")

    # Domanda 9
    print("Domanda 9:")
    print("Si consideri questo pseudo-codice:")
    print("Shared data: boolean lock = false;")
    print("Processo Pi:")
    print("do {")
    print("    while (TestAndSet(&lock));")
    print("    sezione critica")
    print("    lock = false;")
    print("    sezione non critica")
    print("} while (true);")
    print("Di questo pseudo-codice possiamo dire che:")
    print("a. Produce uno spreco inutile di tempo di CPU, perché un processo in attesa di entrare in una sezione critica già occupata passa tutto il suo quanto di tempo a testare la variabile di lock.")
    print("b. Costituisce una soluzione corretta al problema della sezione critica, ha però il difetto di essere basato sul busy-waiting, e dunque di far sprecare inutilmente del tempo di CPU.")
    print("c. Non garantisce la condizione di progresso, perché ogni processo Pi che tentasse di acquisire il lock quando gli viene assegnata la CPU potrebbe trovare la sezione critica sempre occupata da un altro processo.")
    print("d. Non garantisce la mutua esclusione, dato che manca l'istruzione per settare a 1 la variabile di lock e dunque segnalare agli altri processi che è stato acquisito il lock e la sezione critica è occupata.")
    answer9 = input("La tua risposta (a/b/c/d): ").strip().lower()
    if answer9 == "a":
        print("Corretto!\n")
        score += 1
    else:
        print("Sbagliato! La risposta corretta è: a\n")

    # Domanda 10
    print("Domanda 10:")
    print("Si consideri l'esecuzione della seguente porzione di codice che utilizza la system call fork:")
    print("int a, b, c, d, n, pid1, pid2, pid3;")
    print("a = 20, b = 30, c = 40, d = 50;")
    print("n = fork();")
    print("if (n == 0) {")
    print("    a = 25; b = 35;")
    print("    pid1 = getppid();")
    print("    printf('%d', pid1);")
    print("    exit(0);")
    print("} else {")
    print("    c = 45; d = 55;")
    print("    pid2 = getpid();")
    print("    printf('%d', pid2);")
    print("    pid3 = wait(NULL);")
    print("    exit(0);")
    print("}")
    print("Il valore della variabile a vista dal processo figlio subito prima della sua exit è:")
    print("a. 25")
    print("b. 20")
    print("c. 35")
    print("d. 30")
    answer10 = input("La tua risposta (a/b/c/d): ").strip().lower()
    if answer10 == "a":
        print("Corretto!\n")
        score += 1
    else:
        print("Sbagliato! La risposta corretta è: a. 25\n")

    # Domanda 11
    print("Domanda 11:")
    print("Ricostruite il codice della system call Signal:")
    print("signal(semaforo *S) {")
    print("    S->valore++;")
    print("    if (S->valore <= 0) {")
    print("        togli un processo P da S->waiting_list;")
    print("        wakeup(P);")
    print("    }")
    print("}")
    print("Quale delle seguenti affermazioni è corretta?")
    print("a. Il codice è corretto.")
    print("b. Manca l'istruzione per decrementare S->valore.")
    print("c. Manca l'istruzione per aggiungere un processo alla waiting_list.")
    print("d. Il codice non garantisce la mutua esclusione.")
    answer11 = input("La tua risposta (a/b/c/d): ").strip().lower()
    if answer11 == "a":
        print("Corretto!\n")
        score += 1
    else:
        print("Sbagliato! La risposta corretta è: a\n")

    # Risultato finale
    print(f"Hai totalizzato {score} punti su 11!")

# Esegui il quiz
quiz()