// static/js/background.js - 创建动态星空和粒子背景
class DynamicBackground {
    constructor() {
        this.starsContainer = document.getElementById('stars');
        this.particlesContainer = document.getElementById('particles');
        this.meteorsContainer = document.getElementById('meteors');
        this.init();
    }

    init() {
        this.createStars();
        this.createParticles();
        this.createMeteors();
    }

    createStars() {
        const starCount = 150;
        
        for (let i = 0; i < starCount; i++) {
            const star = document.createElement('div');
            star.className = 'star';
            
            // 随机位置
            const x = Math.random() * 100;
            const y = Math.random() * 100;
            
            // 随机大小 (1-3px)
            const size = 1 + Math.random() * 2;
            
            // 随机透明度
            const opacity = 0.1 + Math.random() * 0.3;
            
            // 随机动画时长
            const duration = 3 + Math.random() * 5;
            
            star.style.cssText = `
                left: ${x}%;
                top: ${y}%;
                width: ${size}px;
                height: ${size}px;
                --opacity: ${opacity};
                --duration: ${duration}s;
                animation-delay: ${Math.random() * 5}s;
            `;
            
            this.starsContainer.appendChild(star);
        }
    }

    createParticles() {
        const particleCount = 20;
        
        for (let i = 0; i < particleCount; i++) {
            const particle = document.createElement('div');
            particle.className = 'particle';
            
            // 随机位置
            const x = Math.random() * 100;
            const y = Math.random() * 100;
            
            // 随机大小
            const size = 100 + Math.random() * 200;
            
            // 随机动画延迟
            const delay = Math.random() * 20;
            
            particle.style.cssText = `
                left: ${x}%;
                top: ${y}%;
                width: ${size}px;
                height: ${size}px;
                animation-delay: ${delay}s;
            `;
            
            this.particlesContainer.appendChild(particle);
        }
    }

    createMeteors() {
        const meteorCount = 5;
        
        for (let i = 0; i < meteorCount; i++) {
            const meteor = document.createElement('div');
            meteor.className = 'meteor';
            
            // 随机起始位置
            const startX = Math.random() * 100;
            const startY = Math.random() * 50;
            
            // 随机动画时长
            const duration = 1 + Math.random() * 2;
            
            // 随机延迟
            const delay = Math.random() * 10;
            
            meteor.style.cssText = `
                left: ${startX}%;
                top: ${startY}%;
                --meteor-duration: ${duration}s;
                animation-delay: ${delay}s;
            `;
            
            this.meteorsContainer.appendChild(meteor);
        }
    }
}

// 页面加载完成后初始化背景
document.addEventListener('DOMContentLoaded', function() {
    new DynamicBackground();
});