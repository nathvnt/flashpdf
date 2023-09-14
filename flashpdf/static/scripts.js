let currentCardIndex = 0;
let cards = document.querySelectorAll('.card');

function displayFileName() {
  const input = document.getElementById('file-input');
  const fileNameSpan = document.getElementById('selectedFileName');

  if (input.files.length > 0) {
      fileNameSpan.textContent = input.files[0].name;
  } else {
      fileNameSpan.textContent = '';
  }
}

function flipCard(element) {
  const card = element.closest('.card');
  card.classList.toggle('flipped');
}

function unflipAllCards() {
  cards.forEach(card => {
    card.classList.remove('flipped');
  });
}

function showCard(index) {
  cards.forEach((card, idx) => {
    if (idx === index) {
      card.style.zIndex = '1';
      card.style.opacity = '1';
    } else {
      card.style.zIndex = '0';
      card.style.opacity = '0';
    }
  });
}

function nextCard() {
  unflipAllCards();
  currentCardIndex = (currentCardIndex + 1) % cards.length;
  showCard(currentCardIndex);
}

function prevCard() {
  unflipAllCards();
  currentCardIndex = (currentCardIndex - 1 + cards.length) % cards.length;
  showCard(currentCardIndex);
}

function shuffleArray(array) {
  for (let i = array.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [array[i], array[j]] = [array[j], array[i]];
  }
}

function shuffleCards() {
  unflipAllCards();
  let cardIndices = Array.from(cards.keys());
  shuffleArray(cardIndices);
  cardIndices.forEach((index, i) => {
    cards[index].style.order = i;
  });
  currentCardIndex = 0;
  showCard(currentCardIndex);
}

document.getElementById('totalCards').innerText = cards.length;

function updateCardInfo() {
    document.getElementById('currentCard').innerText = currentCardIndex + 1;
}

function removeCard(element) {
    if (confirm('Are you sure you want to remove this card from the set?')) {
        const card = element.closest('.card');
        card.remove();
        updateCardCount();
        nextCard();
        updateCardsNodeList(); 
    }
}

function updateCardCount() {
    const updatedCards = document.querySelectorAll('.card');
    document.getElementById('totalCards').innerText = updatedCards.length;
    updateCardsNodeList(); 
}

function updateCardsNodeList() {
  cards = document.querySelectorAll('.card');
}

function toggleStudyMode() {
    const isChecked = document.getElementById('studyToggle').checked;
    updateCardsNodeList(); 
    cards.forEach(card => {
        if (isChecked) {
            card.classList.add('start-with-definition');
        } else {
            card.classList.remove('start-with-definition');
        }
    });
}

showCard(currentCardIndex);  // Initialize to show the first card
updateCardInfo(); // Initial card info update
