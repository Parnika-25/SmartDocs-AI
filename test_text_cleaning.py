from backend.text_cleaner import TextCleaner

sample_text = """
######## PAGE 1 ########

   This   is    a     SAMPLE   Text!!!    

Page 1

It contains     excessive     spaces,
special $$$%%% characters, and
MIXED Case Letters.

---

Some unicode text: café naïve résumé

######## PAGE 2 ########
"""

cleaner = TextCleaner()

print("\n" + "=" * 80)
print("BEFORE CLEANING:")
print(sample_text)

cleaned_text = cleaner.clean_text(sample_text)

print("\n" + "=" * 80)
print("AFTER CLEANING:")
print(cleaned_text)
