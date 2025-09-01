import { useState } from 'react';
import { Button } from '@/components/ui/button';
import { PlusCircle, MessageCircle, X, Trash2 } from 'lucide-react';
import { cn } from '@/lib/utils';
import { ScrollArea } from '@/components/ui/scroll-area';
import { Overview } from "./overview";
import { PanelLeftClose } from "lucide-react";

interface SidebarProps {
  isOpen: boolean;
  onClose: () => void;
  onDeleteChat?: (chatId: string) => void;
  onQuestionClick?: (question: string) => void;
  className?: string;
}

export function Sidebar({ isOpen, onClose, onDeleteChat, onQuestionClick, className }: SidebarProps) {
  const [chats, setChats] = useState<{ id: string; name: string; active: boolean }[]>([]);
  const [activeChat, setActiveChat] = useState<string | null>(null);

  const createNewChat = () => {
    const newChat = {
      id: Date.now().toString(),
      name: `Chat ${chats.length + 1}`,
      active: false,
    };
    setChats([...chats, newChat]);
  };

  const selectChat = (chatId: string) => {
    setActiveChat(chatId);
    setChats(chats.map(chat => ({
      ...chat,
      active: chat.id === chatId,
    })));
  };

  const handleDeleteChat = (e: React.MouseEvent, chatId: string) => {
    e.stopPropagation();
    if (onDeleteChat) {
      onDeleteChat(chatId);
      setChats(chats.filter(chat => chat.id !== chatId));
      if (activeChat === chatId) {
        setActiveChat(null);
      }
    }
  };

  return (
    <div
      className={cn(
        "flex flex-col h-full bg-secondary text-secondary-foreground transition-all duration-300 ease-in-out",
        isOpen ? "w-full md:w-80 p-4" : "w-0",
        "overflow-hidden",
        className
      )}
    >
      {isOpen && (
        <>
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-lg font-semibold">Suggestions</h2>
            <Button variant="ghost" size="icon" onClick={onClose} className="md:hidden">
              <PanelLeftClose className="h-5 w-5" />
            </Button>
          </div>
          <Overview onQuestionClick={onQuestionClick} />
        </>
      )}
    </div>
  );
}
