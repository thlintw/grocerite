export enum ItemCategory {
    Vegetables = 'vegetables',
    Fruits = 'fruits',
    MeatAndPoultry = 'meat_and_poultry',
    Seafood = 'seafood',
    DairyAndEggs = 'dairy_and_eggs',
    BakeryAndBread = 'bakery_and_bread',
    FrozenFoods = 'frozen_foods',
    CannedGoodsAndSoup = 'canned_goods_and_soup',
    Staples = 'staples',
    Beverages = 'beverages',
    BeveragesAlcoholic = 'beverages_alcoholic',
    SnacksAndCandy = 'snacks_and_candy',
    CondimentsAndSauces = 'condiments_and_sauces',
    GrainsPastaAndSides = 'grains_pasta_and_sides',
    BreakfastAndCereal = 'breakfast_and_cereal',
    HealthAndBeauty = 'health_and_beauty',
    BabyItems = 'baby_items',
    PetSupplies = 'pet_supplies',
    HouseholdEssentials = 'household_essentials',
    DeliAndPreparedFoods = 'deli_and_prepared_foods',
    SpicesAndSeasonings = 'spices_and_seasonings',
    ToolsAndHomeImprovement = 'tools_and_home_improvement',
    OfficeSupplies = 'office_supplies',
    ToysAndGames = 'toys_and_games',
    Electronics = 'electronics',
    ClothingAndAccessories = 'clothing_and_accessories',
    BooksAndMedia = 'books_and_media',
    Automotive = 'automotive',
    FitnessAndSports = 'fitness_and_sports',
    Other = 'other'
}

export enum ItemIcon {

}

export class Item {
    idx: number;
    name: string;
    category: ItemCategory;
    icon: ItemIcon | null;

    constructor({
        idx = -1,
        name = '',
        category = ItemCategory.Other,
        icon = null
    } : {
        idx?: number,
        name?: string,
        category?: ItemCategory,
        icon?: ItemIcon | null
    } = {}) {
        this.idx = idx;
        this.name = name;
        this.category = category;
        this.icon = icon;
    }

    static fromJson(json: any): Item {
        return new Item({
            idx: json.idx,
            name: json.name,
            category: ItemCategory[json.category],
            icon: json.icon
        });
    }

}
