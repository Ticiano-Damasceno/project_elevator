import '../styles/ElevatorPanel.css';
import type { ReactNode } from 'react';

type Props = {
    children: ReactNode
}

export function ElevatorPanel({ children }: Props) {
    return (
        <div className="panel">            
            {children}
        </div>
    )
}