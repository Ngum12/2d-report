import httpx
from datetime import datetime
from typing import List, Dict, Any, Optional

from app.config import SLACK_WEBHOOK_URL


class SlackService:
    """Service for formatting and sending reports to Slack."""

    # Status emoji mapping
    STATUS_EMOJI = {
        "Completed": "✅",
        "Partially completed": "🔄",
        "Blocked": "⛔"
    }

    # Rank emojis for leaderboard
    RANK_EMOJI = {
        1: "🥇",
        2: "🥈",
        3: "🥉"
    }

    @classmethod
    def format_date(cls, date_str: str) -> str:
        """Format date string to readable format."""
        try:
            dt = datetime.strptime(date_str, "%Y-%m-%d")
            return dt.strftime("%A, %B %d, %Y")
        except ValueError:
            return date_str

    @classmethod
    def get_status_emoji(cls, status: str) -> str:
        """Get emoji for status."""
        return cls.STATUS_EMOJI.get(status, "📋")

    @classmethod
    def get_rank_emoji(cls, rank: int) -> str:
        """Get emoji for rank position."""
        return cls.RANK_EMOJI.get(rank, "  ")

    @classmethod
    def generate_slack_message(
        cls,
        date: str,
        metrics: Dict[str, Any],
        project_summary: List[Dict[str, Any]],
        annotator_summary: List[Dict[str, Any]],
        challenges_list: List[Any],
        task_allocation: str = ""
    ) -> str:
        """Generate formatted Slack message from report data."""
        
        formatted_date = cls.format_date(date)
        
        # Build message parts
        lines = []
        
        # Header
        lines.append(f"📊 *ANNOTATION DAILY HQ* — {formatted_date}")
        lines.append("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        lines.append("")
        
        # Today's Impact
        lines.append("🎯 *TODAY'S IMPACT*")
        lines.append(f"• *{metrics.get('total_images', 0):,}* images processed")
        lines.append(f"• *{metrics.get('total_hours', 0):.1f}* hours invested")
        lines.append(f"• *{metrics.get('annotator_count', 0)}* team members active")
        lines.append(f"• *{len(project_summary)}* projects worked on")
        lines.append("")
        lines.append("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        lines.append("")
        
        # Project Status
        if project_summary:
            lines.append("📋 *PROJECT STATUS*")
            lines.append("")
            
            for project in project_summary:
                project_name = project.get('project_name', 'Unknown')
                total_images = project.get('total_images', 0)
                
                # Determine project status (you might want to track this more precisely)
                # For now, assume completed if there are images
                status_emoji = "✅"
                status_text = "COMPLETE"
                
                lines.append(f"{status_emoji} `{project_name}`")
                lines.append(f"    {total_images} images processed — *{status_text}*")
                lines.append("")
            
            lines.append("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
            lines.append("")
        
        # Team Contributions
        if annotator_summary:
            lines.append("👥 *TEAM CONTRIBUTIONS*")
            lines.append("")
            
            for idx, annotator in enumerate(annotator_summary, 1):
                name = annotator.get('annotator_name', 'Unknown')
                images = annotator.get('total_images', 0)
                hours = annotator.get('total_hours', 0)
                
                # Calculate efficiency
                efficiency = images / hours if hours > 0 else 0
                
                rank_emoji = cls.get_rank_emoji(idx)
                rank_prefix = f"{rank_emoji} " if idx <= 3 else "    "
                
                lines.append(f"{rank_prefix}{name} — {images} images, {hours:.1f} hrs _({efficiency:.1f}/hr)_")
            
            lines.append("")
            lines.append("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
            lines.append("")
        
        # Challenges
        challenges_texts = [c.challenges for c in challenges_list if c.challenges and c.challenges.strip()]
        if challenges_texts:
            lines.append("⚠️ *CHALLENGES REPORTED*")
            for challenge in challenges_texts:
                # Split by newlines and bullet points
                for line in challenge.strip().split('\n'):
                    line = line.strip()
                    if line:
                        # Remove existing bullet if present
                        if line.startswith('•') or line.startswith('-') or line.startswith('*'):
                            line = line[1:].strip()
                        lines.append(f"• {line}")
            lines.append("")
        
        # Suggestions
        suggestions_texts = [c.suggestions for c in challenges_list if c.suggestions and c.suggestions.strip()]
        if suggestions_texts:
            lines.append("💡 *SUGGESTIONS*")
            for suggestion in suggestions_texts:
                for line in suggestion.strip().split('\n'):
                    line = line.strip()
                    if line:
                        if line.startswith('•') or line.startswith('-') or line.startswith('*'):
                            line = line[1:].strip()
                        lines.append(f"• {line}")
            lines.append("")
        
        if challenges_texts or suggestions_texts:
            lines.append("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
            lines.append("")
        
        # Task Allocation (if provided)
        if task_allocation and task_allocation.strip():
            lines.append("📌 *TASK ALLOCATION*")
            for line in task_allocation.strip().split('\n'):
                line = line.strip()
                if line:
                    # Add arrow prefix if not already present
                    if not line.startswith('→') and not line.startswith('->'):
                        line = f"→ {line}"
                    else:
                        line = line.replace('->', '→')
                    lines.append(line)
            lines.append("")
            lines.append("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
            lines.append("")
        
        # Footer with average efficiency
        if annotator_summary:
            total_images = sum(a.get('total_images', 0) for a in annotator_summary)
            total_hours = sum(a.get('total_hours', 0) for a in annotator_summary)
            avg_efficiency = total_images / total_hours if total_hours > 0 else 0
            lines.append(f"_Avg Efficiency: {avg_efficiency:.1f} img/hr_")
        
        return '\n'.join(lines)

    @classmethod
    async def send_to_slack(cls, message: str, webhook_url: Optional[str] = None) -> Dict[str, Any]:
        """Send message to Slack webhook."""
        url = webhook_url or SLACK_WEBHOOK_URL
        
        if not url:
            return {
                "success": False,
                "error": "Slack webhook URL not configured. Please set SLACK_WEBHOOK_URL in config.py or environment variable."
            }
        
        payload = {
            "text": message,
            "mrkdwn": True
        }
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(url, json=payload, timeout=10.0)
                
                if response.status_code == 200:
                    return {"success": True, "message": "Report sent to Slack successfully!"}
                else:
                    return {
                        "success": False,
                        "error": f"Slack API error: {response.status_code} - {response.text}"
                    }
        except httpx.TimeoutException:
            return {"success": False, "error": "Request to Slack timed out"}
        except Exception as e:
            return {"success": False, "error": f"Failed to send to Slack: {str(e)}"}

    @classmethod
    def generate_preview(
        cls,
        date: str,
        metrics: Dict[str, Any],
        project_summary: List[Dict[str, Any]],
        annotator_summary: List[Dict[str, Any]],
        challenges_list: List[Any],
        task_allocation: str = ""
    ) -> str:
        """Generate preview of the Slack message (same as generate but for preview display)."""
        return cls.generate_slack_message(
            date, metrics, project_summary, annotator_summary, challenges_list, task_allocation
        )

