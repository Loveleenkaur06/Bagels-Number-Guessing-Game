import random
import streamlit as st
st.set_page_config(page_title="Bagels - number guessing game", layout="wide")
st.title("Bagels")

NUM_DIGITS = 3  # (!) Try setting this to 1 or 10.
MAX_GUESSES = 10  # (!) Try setting this to 1 or 100.


def main():
    st.text(f'''Bagels, a deductive logic game.
I am thinking of a {NUM_DIGITS}-digit number with no repeated digits.
Try to guess what it is. Here are some clues:
''')
    # Columns appear here
    col1 , = st.columns(1,border=True)
    with col1:
        st.text('''When I say:      |              That means: '''         )
        st.text("""
Pico                    |         One digit is correct but in the wrong position.  

Fermi                 |          One digit is correct and in the right position.  

Bagels               |           No digit is correct.
""")


    st.text("""
For example: If the secret number was 248 and your guess was 843, the clues would be:
Fermi Pico
""")


def getSecretNum():
    """Returns a string made up of NUM_DIGITS unique random digits."""
    numbers = list('0123456789')  # Create a list of digits 0 to 9.
    random.shuffle(numbers)  # Shuffle them into random order.

    # Get the first NUM_DIGITS digits in the list for the secret number:
    secretNum = ''
    for i in range(NUM_DIGITS):
        secretNum += str(numbers[i])
    return secretNum


def getClues(guess, secretNum):
    """Returns a string with the pico, fermi, bagels clues for a guess
    and secret number pair."""
    if guess == secretNum:
        return 'You got it!'

    clues = []

    for i in range(len(guess)):
        if guess[i] == secretNum[i]:
            # A correct digit is in the correct place.
            clues.append('Fermi')
        elif guess[i] in secretNum:
            # A correct digit is in the incorrect place.
            clues.append('Pico')
    if len(clues) == 0:
        return 'Bagels'  # There are no correct digits at all.
    else:
        # Sort the clues into alphabetical order so their original order
        # doesn't give information away.
        clues.sort()
        # Make a single string from the list of string clues.
        return ' '.join(clues)
        # If the program is run (instead of imported), run the game:
if __name__ == '__main__':
    main()
    
    if 'secretNum' not in st.session_state:
        st.session_state.secretNum = getSecretNum()
        st.session_state.numGuesses = 1

    st.write('I have thought up a number.')
    st.write('You have {} guesses to get it.'.format(MAX_GUESSES))
    with st.form("guess_form"):
        guess = st.text_input(
            f"Guess #{st.session_state.numGuesses}",
            max_chars=NUM_DIGITS
        )
        submitted = st.form_submit_button("Submit Guess")

    if submitted:
        if len(guess) != NUM_DIGITS or not guess.isdecimal():
            st.error("Enter a valid {}-digit number.".format(NUM_DIGITS))
        else:
            clues = getClues(guess, st.session_state.secretNum)
            st.write(clues)
            if guess == st.session_state.secretNum:
                st.success("You got it!")
            else:
                st.session_state.numGuesses += 1
                if st.session_state.numGuesses > MAX_GUESSES:
                    st.write('You ran out of guesses.')
                    st.write('The answer was {}.'.format(st.session_state.secretNum))

    if st.button("Play Again"):
        st.session_state.secretNum = getSecretNum()
        st.session_state.numGuesses += 1
        st.rerun()