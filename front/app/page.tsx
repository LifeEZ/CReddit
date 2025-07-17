"use client";

import { ArrowBigDown, ArrowBigUp, MessageSquare, Share2 } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Separator } from "@/components/ui/separator";
import { useState } from "react";
import { posts as initialPosts } from "@/lib/data";
import Link from "next/link";
import { formatNumber } from "@/lib/utils";

export default function Home() {
  const [posts, setPosts] = useState(initialPosts);

  const handleVote = (postId: number, increment: boolean) => {
    setPosts(posts.map(post => {
      if (post.id === postId) {
        return {
          ...post,
          votes: post.votes + (increment ? 1 : -1)
        };
      }
      return post;
    }));
  };

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

      <main className="max-w-5xl mx-auto px-4 py-6 flex gap-6">
        <div className="flex-1 space-y-4">
          {posts.map(post => (
            <Card key={post.id} className="overflow-hidden">
              <div className="flex">
                <div className="bg-gray-50 dark:bg-gray-800 p-2 flex flex-col items-center">
                  <Button
                    variant="ghost"
                    size="icon"
                    onClick={() => handleVote(post.id, true)}
                  >
                    <ArrowBigUp className="h-6 w-6" />
                  </Button>
                  <span className="font-medium text-sm">{formatNumber(post.votes)}</span>
                  <Button
                    variant="ghost"
                    size="icon"
                    onClick={() => handleVote(post.id, false)}
                  >
                    <ArrowBigDown className="h-6 w-6" />
                  </Button>
                </div>
                <div className="p-4 flex-1">
                  <div className="flex items-center text-sm text-gray-500 dark:text-gray-400">
                    <span className="font-medium text-gray-900 dark:text-white">{post.subreddit}</span>
                    <span className="mx-1">•</span>
                    <span>Posted by u/{post.author}</span>
                  </div>
                  <Link href={`/post/${post.id}`}>
                    <h2 className="mt-2 text-xl font-semibold text-gray-900 dark:text-white hover:text-blue-600 dark:hover:text-blue-400">
                      {post.title}
                    </h2>
                  </Link>
                  <p className="mt-2 text-gray-700 dark:text-gray-300">{post.content}</p>
                  {post.image && (
                    <Link href={`/post/${post.id}`}>
                      <img 
                        src={post.image} 
                        alt={post.title}
                        className="mt-4 rounded-lg w-full object-cover max-h-96"
                      />
                    </Link>
                  )}
                  <div className="mt-4 flex items-center gap-4">
                    <Link href={`/post/${post.id}`}>
                      <Button variant="ghost" size="sm" className="text-gray-500">
                        <MessageSquare className="h-4 w-4 mr-2" />
                        {post.comments} Comments
                      </Button>
                    </Link>
                    <Button variant="ghost" size="sm" className="text-gray-500">
                      <Share2 className="h-4 w-4 mr-2" />
                      Share
                    </Button>
                  </div>
                </div>
              </div>
            </Card>
          ))}
        </div>

        <div className="hidden md:block w-80">
          <Card className="p-4">
            <h2 className="font-semibold text-lg mb-4">About Community</h2>
            <p className="text-sm text-gray-600 dark:text-gray-300">
              Welcome to our Reddit clone! This is a demo showing how to build a Reddit-like interface
              using Next.js and shadcn/ui components.
            </p>
            <Separator className="my-4" />
            <div className="space-y-2">
              <div className="flex justify-between text-sm">
                <span>Members</span>
                <span className="font-medium">324,891</span>
              </div>
              <div className="flex justify-between text-sm">
                <span>Online</span>
                <span className="font-medium">1,234</span>
              </div>
            </div>
            <Button className="w-full mt-4">Create Post</Button>
          </Card>
        </div>
      </main>
    </div>
  );
}