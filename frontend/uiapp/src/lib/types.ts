export interface User {
    id: number;
    username: string;
    email: string;
    is_creator: boolean;
    avatar?: string;
    bio?: string;
}

export interface Category {
    id: number;
    name: string;
    slug: string;
    icon?: string;
}

export interface Tag {
    id: number;
    name: string;
}

export interface Component {
    id: number;
    title: string;
    slug: string;
    description: string;
    code_content: Record<string, string>;
    preview_url?: string;
    price: number;
    is_public: boolean;
    created_at: string;
    creator: User;
    category: Category;
    tags: Tag[];
    views: number;
    downloads: number;
    likes_count: number;
    is_liked: boolean;
}
