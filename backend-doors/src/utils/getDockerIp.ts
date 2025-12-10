import { execSync } from 'child_process';

export function getDokcerIp(): string {
    try{
        const output = execSync('wsl ip addr', { encoding: 'utf-8' });
        const lines = output.split('\n').map(l => l.trim());
        const inetLine = lines.find(l => l.includes('inet') && l.includes('global eth0'));

        if(!inetLine){
            console.error('Não foi possível encontrar o IP do REDIS.');
            return '';
        }

        const ip = inetLine.split(' ')[1].replace(/\/.*/, '');
        return ip;
    } catch (err) {
        console.error('Erro ao obter o IP do WSL:', err);
        return '';
    }
}