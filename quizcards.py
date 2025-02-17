import os
import csv
import random

base_dir = "FlashCards"

if not os.path.exists(base_dir):
    os.makedirs(base_dir)

def create_topic(topic_name):
    topic_name = topic_name.replace(" ", "_")
    topic_path = os.path.join(base_dir, f"{topic_name}.csv")
    
    if not os.path.exists(topic_path):
        with open(topic_path, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Vocabularies", "Meaning"])
        print(f"Topic '{topic_name}' created successfully!")
    else:
        print(f"Topic '{topic_name}' already exists!")

def add_words_to_topic(topic_name):
    # Xoá khoảng trắng và tạo tên file hợp lệ
    topic_name = topic_name.replace(" ", "_")
    topic_path = os.path.join(base_dir, f"{topic_name}.csv")
    
    if not os.path.exists(topic_path):
        print(f"Topic '{topic_name}' does not exist. Let's create it first!")
        return
    
    # Đọc từ vựng đã có trong topic
    existing_words = set()
    with open(topic_path, mode="r") as file:
        reader = csv.reader(file)
        next(reader)  # Bỏ qua header
        for word, _ in reader:
            existing_words.add(word.lower())

    print("\nInput word and meaning (Press '0' to finish):")
    words = []
    i = 1
    while True:
        word = input(f"Word ({i}): ").strip()
        if word == "0":
            break
        meaning = input("Meaning: ").strip()
        
        # Kiểm tra trùng từ
        if word.lower() in existing_words:
            print(f"⚠ The word '{word}' already exists in the topic '{topic_name}'. Please enter a different word.")
            continue
        
        words.append((word, meaning))
        existing_words.add(word.lower())
        i += 1

    # Ghi từ mới vào file CSV
    with open(topic_path, mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(words)
    print(f"Added {i - 1} words into topic '{topic_name}.csv'")

def quiz(topic_name):
    topic_name = topic_name.replace(" ", "_")
    topic_path = os.path.join(base_dir, f"{topic_name}.csv")
    
    if not os.path.exists(topic_path):
        print(f"⚠ Topic '{topic_name}' does not exist. Let's create it first!")
        return

    words = []
    with open(topic_path, mode="r") as file:
        reader = csv.reader(file)
        next(reader)  # Bỏ qua header
        words = list(reader)

    if not words:
        print(f"⚠ Topic '{topic_name}' contains no words!")
        return

    correct_count = 0
    random.shuffle(words)

    print("\n🔥 Vocabulary Quiz! Type the meaning:")

    for word, meaning in words:
        answer = input(f"🔹 {meaning}: ").strip()
        if answer.lower() == word.lower():
            print("✅ Great job!")
            correct_count += 1
        else:
            print(f"❌ Wrong! The correct answer is: {word}")

    print(f"\n🎯 You got {correct_count}/{len(words)} correct.")

def show_existing_topics():
    print("\nExisting topics:")
    files = [f.replace(".csv", "") for f in os.listdir(base_dir) if f.endswith(".csv")]
    if files:
        for idx, file in enumerate(files, 1):
            print(f"{idx}. {file}")
        return files
    else:
        print("⚠ No topics available.")
        return []

def main():
    while True:
        print("\n📌 --- MENU ---")
        print("1. Create Topic (Set Flashcard)")
        print("2. Add Vocab")
        print("3. Quiz")
        print("4. Exit")

        choice = input("Menu: ")

        if choice == "1":
            topic_name = input("Enter topic name: ").strip()
            create_topic(topic_name)

        elif choice == "2":
            topics = show_existing_topics()
            if topics:
                try:
                    choice = int(input(f"Enter the number of the topic to add words: "))
                    if 1 <= choice <= len(topics):
                        topic_name = topics[choice - 1]
                        add_words_to_topic(topic_name)
                    else:
                        print("⚠ Invalid choice!")
                except ValueError:
                    print("⚠ Please enter a valid number!")
                
        elif choice == "3":
            topics = show_existing_topics()
            if topics:
                try:
                    choice = int(input(f"Enter the number of the topic to take the quiz: "))
                    if 1 <= choice <= len(topics):
                        topic_name = topics[choice - 1]
                        quiz(topic_name)
                    else:
                        print("⚠ Invalid choice!")
                except ValueError:
                    print("⚠ Please enter a valid number!")
        
        elif choice == "4":
            print("👋 Thanks! See you later!")
            break

        else:
            print("⚠ Invalid choice. Please try again!")

if __name__ == "__main__":
    main()
