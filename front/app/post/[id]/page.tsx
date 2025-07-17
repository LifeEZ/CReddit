import { posts, comments as initialComments } from "@/lib/data";
import { PostContent } from "./post-content";
import { Card } from "@/components/ui/card";
import Link from "next/link";
import { Button } from "@/components/ui/button";
import { Comments } from "./comments";

// Generate static params for all posts
export function generateStaticParams() {
  return posts.map((post) => ({
    id: post.id.toString(),
  }));
}

export default function PostPage({ params }: { params: { id: string } }) {
  const post = posts.find(p => p.id === parseInt(params.id));
  const postComments = initialComments[parseInt(params.id)] || [];

  if (!post) {
    return (
      <div className="min-h-screen bg-gray-50 dark:bg-gray-900 flex items-center justify-center">
        <Card className="p-6">
          <h1 className="text-xl font-semibold">Post not found</h1>
          <Link href="/" className="mt-4 text-blue-600 hover:underline block">
            Return to home
          </Link>
        </Card>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
      <header className="bg-white dark:bg-gray-800 border-b border-gray-200 dark:border-gray-700">
        <div className="max-w-5xl mx-auto px-4 py-3 flex items-center justify-between">
          <Link href="/" className="text-2xl font-bold text-gray-900 dark:text-white">
            reddit clone
          </Link>
          <Button variant="outline">Sign In</Button>
        </div>
      </header>

      <main className="max-w-5xl mx-auto px-4 py-6">
        <PostContent post={post} />
        <Comments comments={postComments} />
      </main>
    </div>
  );
}