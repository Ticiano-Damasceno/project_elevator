import '../styles/ElevatorPanel.css';
import { ReactNode } from 'react';

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