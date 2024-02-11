RENT_PROPERTY_PRICES = [8000, 9000, 10000, 15000, 20000, 25000, 30000]
NON_RENT_PROPERTY_PRICES = [1 * 10**7, 1.5 * 10**7, 2 * 10**7, 2.5 * 10**7, 3 * 10**7]

PROPERTY_TYPE_CHOICES = [
    ('apartment', 'Apartment'),
    ('house', 'House'),
    ('land', 'Land'),
    ('commercial', 'Commercial'),
    ('other', 'Other')
]

PROPERTY_LABEL_CHOICES = [
    ('front', 'Front View'),
    ('back', 'Back View'),
    ('bedroom', 'Bedroom'),
    ('kitchen', 'Kitchen'),
    ('living_room', 'Living Room'),
    ('bathroom', 'Bathroom'),
    ('others', 'Others')
]

ALLOWED_PROPERTY_FILEDS_TO_UPDATE = [
    "title", "description", "price", "bedrooms", "area", "property_type", "bathrooms",
    "documents", "sold"
]